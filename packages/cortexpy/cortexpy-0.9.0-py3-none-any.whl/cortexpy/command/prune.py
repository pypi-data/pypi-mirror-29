"""
cortexpy prune

Usage:
  cortexpy prune --out <graph> <graph> [-t <n>]

Options:
    -h, --help            Display this help message.
    -o, --out <graph>     Output graph.
    -t, --remove-tips <n> Remove tips less than <n>

Description:
    graph            A cortexpy graph.  '-' redirects to or from stdout.
"""
from cortexpy.graph import Interactor


def validate_prune(args):
    from schema import Schema, Use

    schema = Schema({
        '--remove-tips': Use(int),
        str: object,
    })
    return schema.validate(args)


def prune(argv):
    from docopt import docopt
    from cortexpy import VERSION_STRING

    args = docopt(__doc__, argv=argv, version=VERSION_STRING)
    args = validate_prune(args)

    import networkx as nx
    import sys

    if args['--out'] == '-':
        output = sys.stdout.buffer
    else:
        output = open(args['--out'], 'wb')

    if args['<graph>'] == '-':
        graph = nx.read_gpickle(sys.stdin.buffer)
    else:
        graph = nx.read_gpickle(args['<graph>'])

    Interactor(graph, colors=None).prune_tips_less_than(args['--remove-tips'])

    nx.write_gpickle(graph, output)
