#!/usr/bin/python3

from fbmexplorer.parser import parse
from os import walk
import subprocess

with open("messages.json", "w") as f:
    subprocess.call(["fbcap", "html/messages.htm", "-f", "json"], stdout = f)

parse("messages.json")
