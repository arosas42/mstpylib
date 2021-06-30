# Begin-Doc
# Name: setuid.py
# Type: package
# Description: Utility for changing uid of scripts run as root
# End-Doc
import os
import sys
import pwd

__all__ = ["setuid"]

# Begin-Doc
# Name: setuid
# Type: function
# Description: switches uid to a particular user if we are running as root
# End-Doc


def setuid(user):
    target_uid = None
    target_gid = None
    target_home = None

    if isinstance(user, int):
        _, _, target_uid, target_gid, _, target_home, *_ = pwd.getpwuid(user)
    else:
        _, _, target_uid, target_gid, _, target_home, *_ = pwd.getpwnam(user)

    if os.getuid() == 0:
        os.setgid(target_gid)
        os.setuid(target_uid)
        os.environ["HOME"] = target_home

    if (os.getuid(), os.getgid()) != (target_uid, target_gid):
        sys.stderr.write(f"Unable to set uid/gid... Exiting.\n")
        os._exit(-1)
