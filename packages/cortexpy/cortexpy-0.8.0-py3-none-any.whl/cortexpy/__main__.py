"""
cortexpy

Usage: cortexpy [--help] <command> [<args>...]

Options:
   -h, --help  Display this help message

Allowed cortexpy commands are:
   view       View a cortex graph
   assemble   Assemble from a cortex graph
   traverse   Traverse a cortex graph

See 'cortexpy <command>' for more information on a specific command.

"""
import sys
from docopt import docopt
from schema import SchemaError

from cortexpy import VERSION_STRING
import logging

logger = logging.getLogger('cortexpy')


def main_without_argv():
    return main(sys.argv[1:])


def main(argv):
    args = docopt(__doc__, argv=argv, version=VERSION_STRING, options_first=True)

    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'view':
        from cortexpy.command.view import view
        return run_command(view, argv)
    elif args['<command>'] == 'assemble':
        from cortexpy.command.assemble import assemble
        return run_command(assemble, argv)
    elif args['<command>'] == 'traverse':
        from cortexpy.command.traverse import traverse
        return run_command(traverse, argv)
    else:
        print("'{}' is not a cortexpy command. See 'cortexpy --help'.".format(args['<command>']),
              file=sys.stderr)
        return 1


def run_command(function, argv):
    try:
        function(argv)
    except SchemaError as e:
        print('Input argument error for arguments: {}'.format(argv))
        print(e, file=sys.stderr)
        return e
    return 0


if __name__ == '__main__':
    exit(main_without_argv())
