#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers.
"""

from fabric.api import env, run, put, local
from os.path import exists
from datetime import datetime

# Define the servers to connect to
env.hosts = ['100.27.12.226', '100.25.38.188']

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        return True
    except Exception:
        return False

def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
