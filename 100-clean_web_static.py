#!/usr/bin/python3
"""delete out-of-date archives"""
from fabric.api import *
import os

env.hosts = ['3.238.181.140', '3.236.65.72']


def do_clean(number=0):
    """clean database of old archives
        Where number is the no. of archives to keep
    """

    number = 1 if int(number) == 0 else int(number)

    # this arranges the archives from oldest - newest
    archives = sorted(os.listdir("versions"))
    # remove and return the newest
    [archives.pop() for i in range(number)]

    # rm the remaining old archive files after pop
    with lcd("versions"):
        [local('sudo rm ./{}'.format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        # make sure that files are listed from oldest to newest on server
        archives = run('ls -tr').split()
        # the new archive list will now contain only folders starting with web_
        archives = [a for a in archives if 'web_static_' in a]
        [archives.pop() for i in range(number)]
        # seperate the files to keep and remove unwanted
        [run('sudo rm -rf ./{}'.format(a)) for a in archives]
