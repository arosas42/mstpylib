import sys
import socket
import os
import inspect
import re
import getpass
import ttl_cache

IGNORE = False
DEFAULT_TTL = 5
skip_decorators = [('ttl_cache.py', 'fn_wrapped')]
server = None
usage_logger_script = None
usage_logger_owner = None
usage_logger_type = None

def LogAPIUsage(msg=None):
    global server, usage_logger_script, usage_logger_owner, usage_logger_type
    # allow application request that we not log anything
    if IGNORE:
        return

    stack = inspect.stack()[1:]
    func_frame, func_file, func_line, func_name, *_ = stack[0]

    # drill down the stack trace and skip any marked decorators
    for frame in stack[1:]:
        caller_frame, caller_file, caller_line, caller_name, *_ = frame
        if (os.path.basename(caller_file), caller_name) not in skip_decorators:
            break 

    if server is None:
        server = socket.gethostname()

    authuser = None
    cwd = os.getcwd()

    if 'flask' in sys.modules:
        request = sys.modules['flask'].request
        authuser = request.environ.get("REMOTE_USER")
        server = request.host 

    if usage_logger_script is None:
        usage_logger_script = sys.argv[0]

    if usage_logger_owner is None:
        if m := re.search(r'^/local/(.*?)/', usage_logger_script):
            usage_logger_owner = m[1] 

    if usage_logger_type is None:
        if "VSCODE_IPC_HOOK_CLI" in os.environ:
            usage_logger_type = "vscode"
        elif "flask" in sys.modules:
            usage_logger_type = "flask"
        elif "PS1" in os.environ:
            usage_logger_type = "shell"
        else:
            usage_logger_type = "unknown" 


    _SendUsagePacket(
        msg=msg,
        user=getpass.getuser(),
        script=usage_logger_script,
        scriptowner=usage_logger_owner,
        cwd=cwd,
        authuser=authuser,
        server=server,
        function=func_name,
        function_file=func_file,
        caller=caller_name,
        caller_file=caller_file,
        language="python",
        type=usage_logger_type
    )

@ttl_cache(DEFAULT_TTL)
def _SendUsagePacket(**kwargs):
    print(f"LogAPIUsage: {kwargs}")