#!/usr/bin/python3
""" Documentation """
from fabric.api import env, put, run
import os

# Define the IP addresses of your web servers
env.hosts = ["18.234.175.174", "98.84.133.145"]

def do_deploy(archive_path):
    """
    Distributes an archive to web servers and sets up the web static deployment.

    This function performs the following steps:
    1. Checks if the archive file exists at the specified path.
       - If the file does not exist, it returns False.
    2. Uploads the archive to the `/tmp/` directory on the web servers.
    3. Uncompresses the archive to the directory
     `/data/web_static/releases/<archive filename without extension>`.
    4. Deletes the uploaded archive file from the `/tmp/` directory.
    5. Deletes the current symbolic link `/data/web_static/current` on the server.
    6. Creates a new symbolic link `/data/web_static/current`
    pointing to the newly deployed directory.
       - This ensures that the web server serves the new version of the site.
    7. If all operations succeed, it returns True. Otherwise, it returns False.

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
