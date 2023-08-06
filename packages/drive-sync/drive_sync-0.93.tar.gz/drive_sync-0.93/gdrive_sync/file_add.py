from __future__ import absolute_import
from pkg_resources import resource_string
# stores default file address
import os
from os import sys, path
import ntpath
import errno

# set directory for relativistic import
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import edit_config
else:
    from . import edit_config

dir_path = os.path.dirname(os.path.abspath(__file__))


# list of manual addresses
# when launched as non-package
if __package__ is None:
    ver_file = os.path.join(dir_path, "docs/ver_info.txt")
    help_file = os.path.join(dir_path, "docs/readme.txt")
    arg_file = os.path.join(dir_path, "docs/args.txt")
    config_file = os.path.join(dir_path, "config_dicts/config.json")
    mime_dict = os.path.join(dir_path, "config_dicts/mime_dict.json")
    format_dict = os.path.join(dir_path, "config_dicts/formats.json")
# when launched as package
else:
    ver_file = resource_string(__name__, "docs/ver_info.txt")
    help_file = resource_string(__name__, "docs/readme.txt")
    arg_file = resource_string(__name__, "docs/args.txt")
    config_file = resource_string(__name__, "config_dicts/config.json")
    mime_dict = resource_string(__name__, "config_dicts/mime_dict.json")
    format_dict = resource_string(__name__, "config_dicts/formats.json")


# returns credentials file address
def cred_file():

    if __package__ is None:
        return os.path.join(dir_path, "credentials.json")
    else:
        return resource_string(__name__, "credentials.json")



# Making file address for upload and downloads
config = edit_config.read_config()


# Checks if directory present, otherwise make it
def dir_exists(addr):
    if not os.path.exists(addr):
        try:
            os.makedirs(addr)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise


# Returns the current download directory address
def down_addr():
    addr = os.path.join(os.path.expanduser('~'), config['Down_Dir'])
    # making directory if it doesn't exist
    dir_exists(addr)
    return addr


# Returns list with current set upload directories
def up_addr():
    up_addr_list = []
    for addr in config['Up_Dir']:
        # making directory if it doesn't exist
        dir_exists(os.path.join(os.path.expanduser('~'), addr))
        up_addr_list.append(os.path.join(os.path.expanduser('~'), addr))
    return up_addr_list


# Extracts file name or folder name from full path
def get_f_name(addr):
    head, tail = ntpath.split(addr)
    return tail or ntpath.basename(head)  # return tail when file, otherwise other one for folder


# list of manual addresses
share_store = os.path.join(down_addr(), "share_links.txt")


# to eradicate circular import problems
if __name__ == "__main__":
    pass
