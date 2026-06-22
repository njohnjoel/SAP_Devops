import argparse
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sap.host_setup import configure_hostname

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def cmd_configure_hostname(args):
    server_type = args.server
    logger.info(f"Configuring hostname for server type: {server_type}")
    
    success = configure_hostname(server_type)
    
    if success:
        logger.info(f"Successfully configured {server_type}")
        return 0
    else:
        logger.error(f"Failed to configure {server_type}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='SAP Lab Environment Controller',
        prog='sap'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    hostname_parser = subparsers.add_parser(
        'configure_host',
        help='Configure hostname and IP address for a server'
    )
    hostname_parser.add_argument(
        'server',
        help='Server type (appserver, s4hanadb, devops, intranet)'
    )
    hostname_parser.set_defaults(func=cmd_configure_hostname)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        exit_code = args.func(args)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
