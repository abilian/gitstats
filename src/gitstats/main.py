import sys

from .gitstats import GitStats


def main():
    g = GitStats()
    g.run(sys.argv[1:])


if __name__ == "__main__":
    main()
