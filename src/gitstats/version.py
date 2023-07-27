import os
from functools import cache

from .config import gnuplot_cmd
from .utils import getcommitrange, getpipeoutput

VERSION = 0


@cache
def getversion():
    global VERSION
    if VERSION == 0:
        gitstats_repo = os.path.dirname(os.path.abspath(__file__))
        VERSION = getpipeoutput(
            [
                "git --git-dir=%s/.git --work-tree=%s rev-parse --short %s"
                % (gitstats_repo, gitstats_repo, getcommitrange("HEAD").split("\n")[0])
            ]
        )
    return VERSION


@cache
def getgitversion():
    return getpipeoutput(["git --version"]).split("\n")[0]


@cache
def getgnuplotversion():
    return getpipeoutput([f"{gnuplot_cmd} --version"]).split("\n")[0]
