import os
import platform

GNUPLOT_COMMON = "set terminal png transparent size 640,240\nset size 1.0,1.0\n"
ON_LINUX = platform.system() == "Linux"
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

exectime_internal = 0.0
exectime_external = 0.0

# By default, gnuplot is searched from path, but can be overridden with the
# environment variable "GNUPLOT"
gnuplot_cmd = "gnuplot"
if "GNUPLOT" in os.environ:
    gnuplot_cmd = os.environ["GNUPLOT"]

conf = {
    "max_domains": 10,
    "max_ext_length": 10,
    "style": "gitstats.css",
    "max_authors": 20,
    "authors_top": 5,
    "commit_begin": "",
    "commit_end": "HEAD",
    "linear_linestats": 1,
    "project_name": "",
    "processes": 8,
    "start_date": "",
    "verbose": False,
    "text_files_not_read": ["json", "svg", "woff", "woff2"],
}
