# Begin-Doc
# Name: __init__.py
# Type: module
# Description: central entrypoint into the mstpylib module, this file is mainly used for exposing some lower level functions directly into the mstpylib.* scope
#    i.e. mstpylib.setuid.setuid -> mstpylib.setuid
# End-Doc
from mstpylib.setuid import *
from mstpylib.local_env import *
