from data_fetch import DataFetch


class DataFetchCli:

    def __init__(self, subparsers):
        data_fetch_cli_parser = subparsers.add_parser('data_fetch', help='Commands for fetching bluetooth logs')
        data_fetch_cli_parser.add_argument('-s', '--start', action='store_true',
                                           help="Start fetching data")
        data_fetch_cli_parser.add_argument('-t', '--timeout',
                                           help="Set timeout for fetching logs")
        data_fetch_cli_parser.add_argument('-dst', '--destination',
                                           help="Set destination for storing logs")

        data_fetch_cli_parser.set_defaults(func=self.__parse)

        self.__data_fetch = DataFetch()

    def __parse(self, args):
        if args.timeout is not None:
            self.__data_fetch.set_timeout(int(args.timeout))

        if args.destination is not None:
            self.__data_fetch.set_destination(args.destination)

        if args.start:
            self.__data_fetch.start()

