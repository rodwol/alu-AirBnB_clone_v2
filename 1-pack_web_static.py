#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the 'web_static' folder.

    This function performs the following steps:
    1. Defines the source directory as 'web_static' and the
    destination directory as 'versions'.
    2. Checks if the 'versions' directory exists, and if not, it creates the directory.
    3. Creates a timestamp in the format 'YYYYMMDDHHMMSS',
    which is used in the archive name.
    4. Builds the archive name in the format 'web_static_<timestamp>.tgz'
    and constructs the full path where the archive will be saved.
    5. Uses the `local` function from Fabric to create a tarball (`.tgz`)
    of the 'web_static' folder inside the 'versions' directory.
    6. If successful, returns the full path of the generated archive. If any
    error occurs during the process, it prints the error and returns `None`.

    Returns:
        str: The full path to the generated archive if successful.
        None: If an error occurs during the archive creation. 
    """
    
    # Define the source and version directory
    source_folder = 'web_static'
    versions_folder = 'versions'

    # Create the versions directory if it doesn't exist
    if not os.path.exists(versions_folder):
        os.makedirs(versions_folder)

    # Get the current timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = os.path.join(versions_folder, archive_name)

    try:
        # Use the local command to create the .tgz archive
        local(f'tar -cvzf {archive_path} {source_folder}')
        return archive_path
    except Exception as e:
        print(f"Error: {e}")
        return None
