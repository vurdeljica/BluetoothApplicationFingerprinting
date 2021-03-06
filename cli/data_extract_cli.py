from data_extract import DataExtract


class DataExtractCli:

    def __init__(self, subparsers):
        data_extract_cli_parser = subparsers.add_parser('data_extract', help='Commands for extracting bluetooth logs')
        data_extract_cli_parser.add_argument('-s', '--start', action='store_true',
                                            help="Start extracting all data")
        data_extract_cli_parser.add_argument('-file', '--file', action='store_true',
                                            help="Extract data from one file")
        data_extract_cli_parser.add_argument('-src', '--source',
                                            help="Set source file")
        data_extract_cli_parser.add_argument('-dst', '--destination',
                                            help="Set destination for storing logs")

        data_extract_cli_parser.set_defaults(func=self.__parse)

        self.__data_extract = DataExtract()

    def __parse(self, args):
        if args.source is not None:
            self.__data_extract.set_source(args.source)

        if args.destination is not None:
            self.__data_extract.set_destination(args.destination)

        if args.file and args.start:
            print("Invalid configuration")
            return

        if args.file:
            self.__data_extract.extract_single_file()

        if args.start:
            #self.__data_extract.start()
            self.__data_extract.extract_all()
