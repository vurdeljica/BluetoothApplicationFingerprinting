from machine_learning.learning import Learning


class LearningCli:

    def __init__(self, subparsers):
        learning_cli_parser = subparsers.add_parser('learning', help='Commands for machine learning')
        learning_cli_parser.add_argument('-s', '--start', action='store_true',
                                            help="Start learning")
        learning_cli_parser.add_argument('-src', '--source',
                                            help="Set source file")

        learning_cli_parser.set_defaults(func=self.__parse)

        self.__learning = Learning()

    def __parse(self, args):
        if args.source is not None:
            self.__learning.set_source(args.source)

        if args.start:
            self.__learning.start()
