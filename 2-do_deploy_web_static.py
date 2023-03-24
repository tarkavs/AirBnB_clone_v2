#!/usr/bin/python3
"""create fabfile"""
from fabric.api import put, run, env
from fabric.contrib import files
import os

env.hosts = ['3.238.181.140', '3.236.65.72']


def do_deploy(archive_path):
    """deploy function"""
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    temp = archive_path.split('.')[0]
    file_name = temp.split('/')[1]
    dest = data_path + file_name

    try:
        put(archive_path, '/tmp')
        run('sudo mkdir -p {}'.format(dest))
        run('sudo tar -xzf /tmp/{}.tgz -C {}'.format(file_name, dest))
        run('sudo rm -f /tmp/{}.tgz'.format(file_name))
        run('sudo mv {}/web_static/* {}/'.format(dest, dest))
        run('sudo rm -rf {}/web_static/'.format(dest))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(dest))
        return True
    except RuntimeError:
        return False
