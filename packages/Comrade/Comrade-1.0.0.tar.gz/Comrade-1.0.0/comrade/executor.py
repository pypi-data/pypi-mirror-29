from __future__ import print_function
from subprocess import Popen
from .utils import clear_screen
import shlex


def execute(commands):
    clear_screen()
    for command in commands:
        args = shlex.split(command)
        proc = Popen(args, shell=False)
        proc.wait()
