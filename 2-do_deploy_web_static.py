#!/usr/bin/python3
"""
Deploy web static to different servers
 
"""
from fabric.api import env, put, run
import os

# Define the IP addresses of your web servers
env.hosts = ["18.234.175.174", "98.84.133.145"]


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and sets up the web static deployment.

    Args:
        archive_path (str): The path to the archive to deploy.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    
    """


    # Check if the file exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive filename (with and without extension)
        archive_file = archive_path.split('/')[-1]
        archive_no_ext = archive_file.split('.')[0]

        # Define the paths
        tmp_path = "/tmp/{}".format(archive_file)
        releases_folder = "/data/web_static/\
                           releases/{}".format(archive_no_ext)

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, tmp_path)

        # Create the directory where the archive will be uncompressed
        run("mkdir -p {}".format(releases_folder))

        # Uncompress the archive in the releases folder
        run("tar -xzf {} -C {}".format(tmp_path, releases_folder))

        # Move the files from the uncompressed folder to the proper location
        run("mv {}/web_static/* {}".format(releases_folder, releases_folder))

        # Remove the now-empty web_static folder
        run("rm -rf {}/web_static".format(releases_folder))

        # Delete the archive from the server
        run("rm {}".format(tmp_path))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        run("ln -s {} /data/web_static/current".format(releases_folder))

        return True

    except Exception as e:
        return False
