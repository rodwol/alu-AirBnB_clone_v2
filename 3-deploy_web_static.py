#!/usr/bin/python3
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define the IP addresses of your web servers
env.hosts = ["18.234.175.174", "98.84.133.145"]

# Define the username and SSH key for connecting to your servers
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if successful, otherwise returns None.
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        now = datetime.now()
        archive_name = "versions/web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    
    Parameters:
    - archive_path: the path to the archive to be deployed
    
    Returns:
    - True if all operations succeed, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive name and name without extension
        archive_file = archive_path.split('/')[-1]
        archive_no_ext = archive_file.split('.')[0]

        # Define paths
        tmp_path = f"/tmp/{archive_file}"
        releases_folder = f"/data/web_static/releases/{archive_no_ext}"

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, tmp_path)

        # Create the release folder
        run(f"mkdir -p {releases_folder}")

        # Uncompress the archive to the release folder
        run(f"tar -xzf {tmp_path} -C {releases_folder}")

        # Move files from web_static folder to the releases folder
        run(f"mv {releases_folder}/web_static/* {releases_folder}")

        # Delete the now-empty web_static folder
        run(f"rm -rf {releases_folder}/web_static")

        # Delete the archive from the server
        run(f"rm {tmp_path}")

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        run(f"ln -s {releases_folder} /data/web_static/current")

        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

def deploy():
    """
    Creates and distributes an archive to the web servers.
    
    Returns:
    - True if all operations succeed, False otherwise
    """
    # Create the archive using do_pack
    archive_path = do_pack()
    if archive_path is None:
        return False

    # Deploy the created archive using do_deploy
    return do_deploy(archive_path)
