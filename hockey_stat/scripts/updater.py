import argparse
import logging
import sys

from hockey_stat.parsers import update_tournaments
from hockey_stat.storage import save_tournaments

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument("--debug", action="store_true", help="debug logging")

    args = parser.parse_args()
    if args.version:
        logger.info("show version")
        exit(0)

    return args


def main():
    args = parse_args()
    logger.debug("updater %s", args)

    if args.debug:
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    tournaments = update_tournaments()
    save_tournaments(tournaments)


if __name__ == "__main__":
    main()
