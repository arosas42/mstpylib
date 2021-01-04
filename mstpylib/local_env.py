# Begin-Doc
# Name: local_env.py
# Type: package
# Description: Environment detection routine
# End-Doc

import os
import re

detected_env = None

__all__ = ["local_env"]

# Begin-Doc
# Name: local_env
# Type: function
# Description: returns detected environment name
# End-Doc


def local_env():
    global detected_env
    if detected_env is None:
        if "LOCAL_ENV" in os.environ:
            detected_env = os.environ["LOCAL_ENV"]
        else:
            shn = os.uname().nodename
            if re.match("-d\d+$", shn):
                detected_env = "dev"
            elif re.match("-t\d+$", shn):
                detected_env = "test"
            else:
                detected_env = "prod"
    return detected_env
