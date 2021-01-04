# Begin-Doc
# Name: setuid.py
# Type: package
# Description: Utility for changing uid of scripts run as root
# End-Doc
import os
import pwd

__all__ = ["setuid"]

# Begin-Doc
# Name: setuid
# Type: function
# Description: switches uid to a particular user if we are running as root
# End-Doc


def setuid(user):
    target_uid = None
    target_home = None

    if isinstance(user, int):
        target_uid = user
        tmp = pwd.getpwuid(user)
        target_home = tmp[5]
    else:
        tmp = pwd.getpwnam(user)
        target_uid = tmp[2]
        target_home = tmp[5]

    if os.getuid() == 0:
        os.setuid(target_uid)
        os.environ["HOME"] = target_home

    if os.getuid() != target_uid:
        raise Exception(f"Unable to set UID: {user}")
