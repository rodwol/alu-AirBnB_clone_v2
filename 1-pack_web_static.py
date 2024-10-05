#!/usr/bin/python3
""" Documentation """
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the 'web_static' folder.
    
        
    """

    date_time = strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date_time)
    try:
        local("mkdir -p versions")
        local("tar -zcvf {} web_static".format(file_name))
        return file_name
    except Exception as err:
        return None  
