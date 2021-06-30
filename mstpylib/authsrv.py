# Begin-Doc
# Name: authsrv.py
# Type: package
# Description: wrapper around authsrv binaries
# End-Doc
import getpass
import subprocess
from mstpylib.usage_logger import LogAPIUsage

AUTHSRV_DECRYPT = "authsrv-decrypt"

# Begin-Doc
# Name: set_prefix
# Type: function
# Description: Set prefix for authsrv executeables, should end in platform specific path separator
# End-Doc


def set_prefix(path=""):
    global AUTHSRV_DECRYPT
    AUTHSRV_DECRYPT = path + "authsrv-decrypt"

# Begin-Doc
# Name: fetch
# Type: function
# Description: returns stashed password, "user" defaults to the current userid on unix. If running as root, "owner" can be specified.
# End-Doc


def fetch(owner=getpass.getuser(), user=None, instance=None):
    global AUTHSRV_DECRYPT
    LogAPIUsage()

    if owner != getpass.getuser() and getpass.getuser() != "root":
        owner = getpass.getuser()

    if user is None:
        raise Exception(__name__, "(): user must be defined")

    if instance is None:
        raise Exception(__name__, "(): instance must be defined")

    return subprocess.check_output(
        [
            AUTHSRV_DECRYPT,
            owner,
            user,
            instance
        ]
    ).decode('utf-8').rstrip('\r\n')
