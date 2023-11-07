import os
import re
import shlex
import shutil
import subprocess
import sys
import time

from .config import ON_LINUX, conf, exectime_external


def getpipeoutput(cmds, quiet=(not conf["verbose"]), stream=sys.stdout):
    """Standardised method of calling linux commands.

    :param cmds: Command to execute
    :param quiet: Prints commands on standard output if True.
    :param stream: file to print output to.
    :return:
    """
    global exectime_external

    start = time.time()
    if not quiet and ON_LINUX and os.isatty(1):
        print(">> " + " | ".join(cmds)),
        sys.stdout.flush()

    processes = []
    for cmd in cmds:
        cmd_args = shlex.split(cmd)

        stdin = sys.stdin if len(processes) == 0 else processes[-1].stdout
        p = subprocess.Popen(
            cmd_args, stdin=stdin, stdout=subprocess.PIPE, cwd=os.getcwd(),
        )
        processes.append(p)

    stdout, stderr = (stream if stream else b"" for stream in p.communicate())
    if stream == sys.stdout:
        output = stdout
    elif stream == sys.stderr:
        output = stderr
    else:
        raise Exception("Invalid stream")

    for p in processes:
        p.wait()
    end = time.time()
    if not quiet:
        if ON_LINUX and os.isatty(1):
            print("\r")
        print(f"[{end - start:.5f}] >> {' | '.join(cmds)}")
    exectime_external += end - start
    old_output = output
    new_output = old_output.decode("utf-8")
    return str(new_output).strip("\n")


def getlogrange(defaultrange="HEAD", end_only=True):
    commit_range = getcommitrange(defaultrange, end_only)
    if len(conf["start_date"]) > 0:
        return f"--since=\"{conf['start_date']}\" \"{commit_range}\""
    return commit_range


def getcommitrange(defaultrange="HEAD", end_only=False):
    if len(conf["commit_end"]) > 0:
        if end_only or len(conf["commit_begin"]) == 0:
            return conf["commit_end"]
        return f"{conf['commit_begin']}..{conf['commit_end']}"
    return defaultrange


def getkeyssortedbyvalues(dict):
    return map(lambda el: el[1], sorted(map(lambda el: (el[1], el[0]), dict.items())))


# dict['author'] = { 'commits': 512 } - ...key(dict, 'commits')
def getkeyssortedbyvaluekey(d, key):
    return map(lambda el: el[1], sorted(map(lambda el: (d[el][key], el), d.keys())))


def getstatsummarycounts(line):
    numbers = re.findall(r"\d+", line)
    if len(numbers) == 1:
        # neither insertions nor deletions: may probably only happen for "0 files changed"
        numbers.append(0)
        numbers.append(0)
    elif len(numbers) == 2 and line.find("(+)") != -1:
        numbers.append(0)  # only insertions were printed on line
    elif len(numbers) == 2 and line.find("(-)") != -1:
        numbers.insert(1, 0)  # only deletions were printed on line
    return numbers


def getnumoffilesfromrev(time_rev):
    """Get number of files changed in commit."""
    time, rev = time_rev
    return (
        int(time),
        rev,
        int(
            getpipeoutput([f'git ls-tree -r --name-only "{rev}"', "wc -l"]).split("\n")[
                0
            ]
        ),
    )


def getnumoflinesinblob(ext_blob):
    """Get number of lines in blob."""
    ext, blob_id = ext_blob
    return (
        ext,
        blob_id,
        int(getpipeoutput([f"git cat-file blob {blob_id}", "wc -l"]).split()[0]),
    )
