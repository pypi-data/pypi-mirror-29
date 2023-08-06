from nameko.cli.commands import (
    Command
)

class ReloadRun(Command):
    name = 'rrun'

    @staticmethod
    def init_parser(parser):
        parser.add_argument(
            'services', nargs='+',
            metavar='module[:service class]',
            help='python path to one or more service classes to run')

        parser.add_argument(
            '--config', default='',
            help='The YAML configuration file')

        parser.add_argument(
            '--broker', default='pyamqp://guest:guest@localhost',
            help='RabbitMQ broker url')

        parser.add_argument(
            '--backdoor-port', type=int,
            help='Specify a port number to host a backdoor, which can be'
            ' connected to for an interactive interpreter within the running'
            ' service process using `nameko backdoor`.')

        return parser

    @staticmethod
    def main(args):
        from nameko_dev.run import main
        main(args)


cmds = Command.__subclasses__()
