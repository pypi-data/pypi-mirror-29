"""
cortexpy traverse

Usage:
  cortexpy traverse <graph> --out <file> [options]

Options:
    -h, --help                    Display this help message.
    --out <file>                  Output graph. '-' prints to stdout
    --orientation <orientation>   Traversal orientation [default: both].
    -c --colors <colors>          Colors to traverse [default: 0].
           May take multiple color numbers separated by a comma (example: '0,2,3').
           The traverser will follow all colors specified.
    --max-nodes <n>               Maximum number of nodes to traverse [default: 1000].
    --initial-contig <initial_contig>              Initiate traversal from each k-mer in this string
    --initial-contig-fasta <initial_contig_fasta>  Initiate traversal from each k-mer in this fasta

Description:
    Traverse a cortex graph starting from each k-mer in an initial_contig and return the subgraph as
    a Python pickle object.
"""
import sys
from docopt import docopt
from schema import Schema, Use, Optional
import logging

logger = logging.getLogger('cortexpy.traverse')


def validate(args):
    from cortexpy.graph import traversal
    schema = Schema({
        Optional('--orientation'): (
            lambda x: x in traversal.constants.EngineTraversalOrientation.__members__.keys()
        ),
        Optional('--colors'): Use(lambda colors: [int(color) for color in colors.split(',')]),
        Optional('--max-nodes'): Use(int),
        str: object,
    })
    return schema.validate(args)


def traverse(argv):
    from cortexpy import VERSION_STRING

    args = docopt(__doc__, argv=argv, version=VERSION_STRING)
    args = validate(args)
    if args['--out'] == '-':
        output = sys.stdout.buffer
    else:
        output = open(args['--out'], 'wb')

    import networkx as nx
    from cortexpy.graph import parser as g_parser, traversal
    graph = traversal.Engine(
        g_parser.RandomAccess(open(args['<graph>'], 'rb')),
        traversal_colors=args['--colors'],
        orientation=traversal.constants.EngineTraversalOrientation[
            args['--orientation']],
        max_nodes=args['--max-nodes'],
    ).traverse_from_each_kmer_in(args['--initial-contig']).graph
    nx.write_gpickle(graph, output)
