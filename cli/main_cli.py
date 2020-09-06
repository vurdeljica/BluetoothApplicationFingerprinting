import argparse
import fix_imports
from data_extract_cli import DataExtractCli
from data_fetch_cli import DataFetchCli


def main(command_line=None):
    parser = argparse.ArgumentParser('Bluetooth application fingerprinting cli interface')
    subparsers = parser.add_subparsers(dest='command')

    DataExtractCli(subparsers)
    DataFetchCli(subparsers)

    args = parser.parse_args(command_line)
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == '__main__':
    main()
