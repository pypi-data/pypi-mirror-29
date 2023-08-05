import copy

import attr
import collections
import networkx as nx

from cortexpy import graph
from cortexpy.graph.parser.kmer import EmptyKmerBuilder
from .constants import EngineTraversalOrientation
from . import branch
from cortexpy.graph.serializer import SERIALIZER_GRAPH
from cortexpy.constants import EdgeTraversalOrientation
import logging

logger = logging.getLogger(__name__)


@attr.s(slots=True)
class Engine(object):
    ra_parser = attr.ib()
    traversal_colors = attr.ib((0,))
    orientation = attr.ib(EngineTraversalOrientation.original)
    max_nodes = attr.ib(1000)
    branch_queue = attr.ib(attr.Factory(collections.deque))
    graph = attr.ib(attr.Factory(SERIALIZER_GRAPH))
    queuer = attr.ib(init=False)
    branch_traverser = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._add_graph_metadata()

    def clear(self):
        self.graph.clear()
        self.__attrs_post_init__()

    def traverse_from_each_kmer_in(self, contig):
        kmer_size = self.ra_parser.header.kmer_size
        assert len(contig) >= kmer_size
        for start in range(len(contig) - kmer_size + 1):
            start_kmer = contig[start:(start + kmer_size)]
            try:
                self.graph = nx.compose(
                        self.graph,
                        self._traverse_from(start_kmer).graph
                )
            except KeyError:
                pass
            if len(self.graph) > self.max_nodes:
                logger.warning(("Terminating contig traversal after kmer {}"
                                " because max node limit is reached").format(start_kmer))
                break
        self._post_process_graph()
        return self

    def traverse_from(self, start_string):
        self._traverse_from(start_string)
        self._post_process_graph()
        return self

    def _traverse_from(self, start_string):
        assert len(start_string) == self.ra_parser.header.kmer_size
        self.branch_traverser = {
            color: branch.Traverser(self.ra_parser, traversal_color=color)
            for color in self.traversal_colors
        }
        self.queuer = branch.Queuer(self.branch_queue,
                                    traversal_colors=self.traversal_colors,
                                    engine_orientation=self.orientation)

        self._process_initial_branch(start_string)
        while 0 < len(self.branch_queue) and len(self.graph) < self.max_nodes:
            self._traverse_a_branch_from_queue()
        if len(self.graph) > self.max_nodes:
            logger.warning(
                    "Max nodes ({}) exceeded: {} nodes found".format(self.max_nodes,
                                                                     len(self.graph)))
        return self

    def _post_process_graph(self):
        self.graph = annotate_kmer_graph_edges(self.graph)

    def _add_graph_metadata(self):
        self.graph.graph['colors'] = self.ra_parser.header.colors
        self.graph.graph['sample_names'] = [n.decode() for n in self.ra_parser.header.sample_names]

    def _process_initial_branch(self, start_string):
        if self.orientation == EngineTraversalOrientation.both:
            first_traversal_orientation = EdgeTraversalOrientation.original
        else:
            first_traversal_orientation = EdgeTraversalOrientation[self.orientation.name]
        self.queuer.add_from(start_string,
                             first_traversal_orientation,
                             connecting_node=None,
                             traversal_color=self.traversal_colors[0])
        self._traverse_a_branch_from_queue()
        start_kmer = self.ra_parser.get_kmer_for_string(start_string)
        if self.orientation == EngineTraversalOrientation.both:
            for color in self.traversal_colors:
                oriented_edge_set = start_kmer.edges[color].oriented(
                        EdgeTraversalOrientation.reverse)
                kmer_strings = oriented_edge_set.neighbor_kmer_strings(start_string)
                if len(kmer_strings) == 1:
                    self.queuer.add_from(start_string=kmer_strings[0],
                                         orientation=EdgeTraversalOrientation.reverse,
                                         connecting_node=start_string,
                                         traversal_color=color)
        for color in self.traversal_colors[1:]:
            oriented_edge_set = start_kmer.edges[color].oriented(first_traversal_orientation)
            kmer_strings = oriented_edge_set.neighbor_kmer_strings(start_string)
            for kmer_string in kmer_strings:
                self.queuer.add_from(start_string=kmer_string,
                                     orientation=first_traversal_orientation,
                                     connecting_node=start_string,
                                     traversal_color=color)

    def _traverse_a_branch_from_queue(self):
        setup = self.branch_queue.popleft()
        color_branch_traverser = self.branch_traverser[setup.traversal_color]
        branch = color_branch_traverser.traverse_from(setup.start_string,
                                                      orientation=setup.orientation,
                                                      parent_graph=self.graph)
        self.graph = nx.union(self.graph, branch.graph)
        self._connect_branch_to_parent_graph(branch, setup)
        self._link_branch_and_queue_neighbor_traversals(branch)

    def _connect_branch_to_parent_graph(self, branch, setup):
        if setup.connecting_node is not None and not branch.is_empty():
            self._add_edge_in_orientation(setup.connecting_node, branch.first_kmer_string,
                                          setup.orientation)

    def _link_branch_and_queue_neighbor_traversals(self, branch):
        branch = self._add_neighbors_from_other_colors_to_branch(branch)
        orientations_and_kmer_strings = [(branch.orientation, branch.neighbor_kmer_strings)]
        if self.orientation == EngineTraversalOrientation.both:
            orientations_and_kmer_strings.append(
                    (EdgeTraversalOrientation.other(branch.orientation),
                     branch.reverse_neighbor_kmer_strings)
            )
        for orientation, kmer_strings in orientations_and_kmer_strings:
            for neighbor_string in kmer_strings:
                if neighbor_string in self.graph:
                    self._add_edge_in_orientation(branch.last_kmer_string,
                                                  neighbor_string,
                                                  orientation)
                else:
                    self.queuer.add_from_branch(branch)

    def _add_neighbors_from_other_colors_to_branch(self, branch):
        if branch.is_empty():
            return branch
        last_kmer_string = branch.last_kmer_string
        last_kmer = self.ra_parser.get_kmer_for_string(last_kmer_string)
        neighbor_kmer_strings = set(branch.neighbor_kmer_strings)
        reverse_neighbor_kmer_strings = set(branch.reverse_neighbor_kmer_strings)
        for traversal_color in self.traversal_colors:
            oriented_edge_set = last_kmer.edges[traversal_color].oriented(branch.orientation)
            neighbor_kmer_strings |= set(oriented_edge_set.neighbor_kmer_strings(last_kmer_string))
            reverse_neighbor_kmer_strings |= set(
                    oriented_edge_set.other_orientation().neighbor_kmer_strings(last_kmer_string))

        branch = copy.copy(branch)
        branch.neighbor_kmer_strings = list(neighbor_kmer_strings)
        branch.reverse_neighbor_kmer_strings = list(reverse_neighbor_kmer_strings)
        return branch

    def _add_edge_in_orientation(self, kmer1_string, kmer2_string, orientation):
        if orientation == EdgeTraversalOrientation.reverse:
            kmer1_string, kmer2_string = kmer2_string, kmer1_string
        kmer1 = self.ra_parser.get_kmer_for_string(kmer1_string)
        kmer2 = self.ra_parser.get_kmer_for_string(kmer2_string)
        interactor = graph.Interactor(self.graph, kmer1.colors)
        interactor.add_edge_to_graph_for_kmer_pair(kmer1, kmer2, kmer1_string, kmer2_string)


def annotate_kmer_graph_edges(graph):
    """Adds nodes to graph for kmer_strings that only exist as edges in a node's kmer."""
    colors = graph.graph['colors']
    graph2 = graph.copy()
    for kmer_string, kmer in graph.nodes(data='kmer'):
        for color in colors:
            for new_kmer_string in kmer.edges[color].get_outgoing_kmer_strings(kmer_string):
                graph2.add_edge(kmer_string, new_kmer_string, key=color)
            for new_kmer_string in kmer.edges[color].get_incoming_kmer_strings(kmer_string):
                graph2.add_edge(new_kmer_string, kmer_string, key=color)
    graph3 = graph2.copy()
    kmer_builder = EmptyKmerBuilder(num_colors=len(colors))
    for kmer_string, data in graph2.nodes(data=True):
        if 'kmer' not in data:
            graph3.add_node(kmer_string, kmer=kmer_builder.build_or_get(kmer_string), **data)
    return graph3
