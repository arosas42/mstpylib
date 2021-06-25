# Begin-Doc
# Name: privsys.py
# Type: package
# Description: Privsys namespace 
# End-Doc
from mstpylib.simplerpc import SimpleRPCClient
from mstpylib import local_env, authsrv
import ttl_cache
import re

DEFAULT_TTL = 60
PUBLIC_RPC = None


def simple_public_rpc():
    global PUBLIC_RPC
    if PUBLIC_RPC is not None:
        return PUBLIC_RPC

    rpchost = "https://itrpc-privsys-dev.mst.edu"
    env = local_env()

    if env == "test":
        rpchost = "https://itrpc-privsys-test.mst.edu"
    elif env == "prod":
        rpchost = "https://itrpc-privsys.mst.edu"

    PUBLIC_RPC = SimpleRPCClient(base_url=f"{rpchost}/perl-bin")
    return PUBLIC_RPC

# Begin-Doc
# Name: check_priv
# Type: method
# Description: checks if "user" has priv grants to "code"
# End-Doc


@ttl_cache(DEFAULT_TTL)
def check_priv(user, code):
    rpc = simple_public_rpc()
    val = rpc.CheckPriv(user=user, code=code)
    return val[0] == 1

# Begin-Doc
# Name: check_priv
# Type: method
# Description: checks if "user" has any priv grants that match "regex"
# End-Doc

@ttl_cache(DEFAULT_TTL)
def check_priv_regex(user, regex):
    rpc = simple_public_rpc()
    privs = fetch_privs(user)
    privs.extend(fetch_privs("public"))

    for priv in privs:
        if match := re.search(regex, priv):
            return True

    return False


# Begin-Doc
# Name: fetch_privs
# Type: method
# Description: grabs all privs "user" has currently granted
# End-Doc


@ttl_cache(DEFAULT_TTL)
def fetch_privs(user):
    rpc = simple_public_rpc()
    return rpc.FetchPrivs(user=user)
