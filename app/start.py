"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    Stats scrap <url>
    Stats (-i | --interactive)
    Stats (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from scrapper import scrap_for_mutual_matches


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Unknown Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = 'SPORTSTATS' \
        + ' (you can type help for a list of commands.)'
    prompt = '(stats) '

    @docopt_cmd
    def do_scrap(self, arg):
        """ Usage: scrap <url>"""
        url = arg['<url>']
        scrap_for_mutual_matches(url)

    @docopt_cmd
    def do_quit(self, arg):
        """ Quits out of Interactive Mode."""
        print('See ya, around!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)