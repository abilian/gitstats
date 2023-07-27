#!/usr/bin/env python3
# Copyright (c) 2007-2014 Heikki Hokkanen <hoxu@users.sf.net> & others (see doc/AUTHOR)
# GPLv2 / GPLv3

import getopt
import os
import sys
import time

from .collector import GitDataCollector
from .config import conf, exectime_external
from .report import HTMLReportCreator
from .version import getgnuplotversion

os.environ["LC_ALL"] = "C"
time_start = time.time()


def usage():
    print(
        f"""
Usage: gitstats [options] <gitpath..> <outputpath>

Options:
-c key=value     Override configuration value

Default config values:
{conf}

Please see the manual page for more details.
"""
    )


class GitStats:
    @staticmethod
    def run(args_orig):
        optlist, args = getopt.getopt(args_orig, "hc:", ["help"])
        for o, v in optlist:
            if o == "-c":
                key, value = v.split("=", 1)
                if key not in conf:
                    raise KeyError(f'no such key "{key}" in config')
                if isinstance(conf[key], int):
                    conf[key] = int(value)
                else:
                    conf[key] = value
            elif o in ("-h", "--help"):
                usage()
                sys.exit()

        if len(args) < 2:
            usage()
            sys.exit(0)

        outputpath = os.path.abspath(args[-1])
        rundir = os.getcwd()

        try:
            os.makedirs(outputpath)
        except OSError:
            pass
        if not os.path.isdir(outputpath):
            print("FATAL: Output path is not a directory or does not exist")
            sys.exit(1)

        if not getgnuplotversion():
            print("gnuplot not found")
            sys.exit(1)

        print(f"Output path: {outputpath}")
        cachefile = os.path.join(outputpath, "gitstats.cache")

        data = GitDataCollector()
        data.loadCache(cachefile)

        for gitpath in args[0:-1]:
            print(f"Git path: {gitpath}")

            prevdir = os.getcwd()
            os.chdir(gitpath)

            print("Collecting data...")
            data.collect(gitpath)

            os.chdir(prevdir)

        print("Refining data...")
        data.saveCache(cachefile)
        data.refine()

        os.chdir(rundir)

        print("Generating report...")
        report = HTMLReportCreator()
        report.create(data, outputpath)

        time_end = time.time()
        exectime_internal = time_end - time_start
        print(
            "Execution time %.5f secs, %.5f secs (%.2f %%) in external commands)"
            % (
                exectime_internal,
                exectime_external,
                (100.0 * exectime_external) / exectime_internal,
            )
        )
        if sys.stdin.isatty():
            print("You may now run:")
            print()
            path = os.path.join(outputpath, "index.html").replace("'", "'\\''")
            print(f"   sensible-browser '{path}'")
            print()
