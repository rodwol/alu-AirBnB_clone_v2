#!/usr/bin/python3
""" Documentation """
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the 'web_static' folder.
    
        
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
