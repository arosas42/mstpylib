import sys
import os
import inspect

IGNORE = False
skip_decorators = [('ttl_cache.py', 'fn_wrapped')]

def LogAPIUsage():
    # allow application request we not log anything
    if IGNORE:
        return

    stack = inspect.stack()[1:]
    func_frame, func_file, func_line, func_name, *_ = stack[0]

    # drill down the stack trace and skip any marked decorators
    for frame in stack[1:]:
        caller_frame, caller_file, caller_line, caller_name, *_ = frame
        if (os.path.basename(caller_file), caller_name) not in skip_decorators:
            break 

    send = False