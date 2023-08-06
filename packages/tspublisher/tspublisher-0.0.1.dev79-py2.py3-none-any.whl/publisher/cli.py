from __future__ import print_function

import argparse
import sys
from publisher import git


class PublisherCLI():

    def __init__(self, args):
        parser = argparse.ArgumentParser(
            description='Touch Surgery Publisher',
            usage='tspub <command> [<args>]'
        )
        subparsers = parser.add_subparsers(
            title='Available commands',
            description=(
                'These commands allow you to create and '
                'publish TS simulations'
            ),
            help='subparsers help'
        )
        cli_commands = [c for c in dir(self) if not c.startswith('_')]

        for command in cli_commands:
            sub_parser = subparsers.add_parser(
                command,
                help=getattr(self, command).__doc__
            )
            sub_parser.set_defaults(func=getattr(self, command))

        namespace = parser.parse_args(args[0:1])
        namespace.func(args[1:])

    def setup(self, args):
        """ Setup your machine, ready to create and edit simulations in 3 steps
                1. Check if git is installed
                2. Setup SSH
                3. Cloning the repo and git pull
        """
        git.setup_users_machine()

    def procedures(self, args):
        """ List all procedures in the git repository, each being a separate branch
        """
        git.list_procedures()

    def workon(self, args):
        """ Move to the branch containing the specified procedure so that it can be worked on
        """
        parser = argparse.ArgumentParser(
            description="Move to the branch containing the specified procedure",
            usage='''tspub workon <procedure_code>'''
        )
        parser.add_argument(
            'procedure',
            help="The procedure code"
        )

        args = parser.parse_args(args)
        git.change_procedure(args.procedure)


def main():
    PublisherCLI(sys.argv[1:])
