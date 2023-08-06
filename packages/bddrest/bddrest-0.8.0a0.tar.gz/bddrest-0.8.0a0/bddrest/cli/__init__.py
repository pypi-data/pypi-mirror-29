import sys

from .launchers import Launcher, RequireSubCommand


class MainLauncher(Launcher):

    def __init__(self):
        self.parser = parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            description='bddrest command line interface.'
        )

        subparsers = parser.add_subparsers(
            title="Sub Commands",
            prog=basename(sys.argv[0]),
            dest="command"
        )

#         from restfulpy.mockupservers import SimpleMockupServerLauncher
#         SimpleMockupServerLauncher.register(subparsers)

        argcomplete.autocomplete(parser)

    def launch(self, args=None):
        cli_args = self.parser.parse_args(args if args else None)
        if hasattr(cli_args, 'func'):
            cli_args.func(cli_args)
        else:
            self.parser.print_help()
        sys.exit(0)

    @classmethod
    def create_parser(cls, subparsers):
        """
        Do nothing here
        """
        pass

