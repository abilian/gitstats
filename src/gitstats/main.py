import sys

from .gitstats import GitStats


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    g = GitStats()
    g.run(args)


if __name__ == "__main__":
    main()
