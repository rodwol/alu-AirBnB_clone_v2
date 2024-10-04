#!/usr/bin/python3
from fabric.api import env, put, run
import os

# Define the IP addresses of your web servers
env.hosts = ["18.234.175.174", "98.84.133.145"]

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    
    Parameters:
    - archive_path: the path to the archive to be deployed
    
    Returns:
    - True if all operations succeed, False otherwise
    """
    
    # Check if the file exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive filename (with and without extension)
        archive_file = archive_path.split('/')[-1]
        archive_no_ext = archive_file.split('.')[0]

        # Define the paths
        tmp_path = f"/tmp/{archive_file}"
        releases_folder = f"/data/web_static/releases/{archive_no_ext}"

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, tmp_path)

        # Create the directory where the archive will be uncompressed
        run(f"mkdir -p {releases_folder}")

        # Uncompress the archive in the releases folder
        run(f"tar -xzf {tmp_path} -C {releases_folder}")

        # Move the files from the uncompressed folder to the proper location
        run(f"mv {releases_folder}/web_static/* {releases_folder}")

        # Remove the now-empty web_static folder
        run(f"rm -rf {releases_folder}/web_static")

        # Delete the archive from the server
        run(f"rm {tmp_path}")

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        run(f"ln -s {releases_folder} /data/web_static/current")

        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
