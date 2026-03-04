import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    pass


if __name__ == "__main__":
    main()
