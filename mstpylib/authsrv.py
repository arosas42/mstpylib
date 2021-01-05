# Begin-Doc
# Name: authsrv.py
# Type: package
# Description: wrapper around authsrv binaries
# End-Doc
import getpass
import subprocess

# Begin-Doc
# Name: fetch
# Type: function
# Description: returns stashed password, "user" defaults to the current userid on unix. If running as root, "owner" can be specified.
# End-Doc


def fetch(owner=getpass.getuser(), user=None, instance=None):
    if owner != getpass.getuser() and getpass.getuser() != "root":
        owner = getpass.getuser()

    if user is None:
        raise Exception(__name__, "(): user must be defined")

    if instance is None:
        raise Exception(__name__, "(): instance must be defined")

    return subprocess.getoutput(f"authsrv-raw-decrypt {owner} {user} {instance}")
