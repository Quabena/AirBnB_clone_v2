#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives.

Execute: fab -f 100-clean_web_static.py do_clean:number=<number>
-i <ssh_key> -u <user>
"""

from fabric.api import env, local, run
from os.path import isdir
env.hosts = ['100.27.12.226', '100.25.38.188']


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    :param number: Number of archives to keep.
    """
    number = int(number)
    if number < 1:
        number = 1

    # Local cleanup
    if isdir("versions"):
        local_archives = sorted(local("ls -tr versions", capture=True).split())
        archives_to_delete = local_archives[:-number]
        for archive in archives_to_delete:
            local("rm -f versions/{}".format(archive))

    # Remote cleanup
    remote_path = "/data/web_static/releases"
    remote_archives = run("ls -tr {}".format(remote_path)).split()
    remote_archives = [arc for arc in remote_archives if "web_static_" in arc]
    archives_to_delete = remote_archives[:-number]
    for archive in archives_to_delete:
        run("rm -rf {}/{}".format(remote_path, archive))
