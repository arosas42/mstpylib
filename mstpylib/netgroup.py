# Begin-Doc
# Name: netgroup.py
# Type: package
# Description: Package/wrapper around Netgroup RPC calls
# End-Doc
from mstpylib.simplerpc import SimpleRPCClient
from mstpylib import local_env
import ttl_cache

DEFAULT_TTL = 60
netgroup_rpc = None
rpc_auth_user = None
rpc_auth_pass = None

# Begin-Doc
# Name: login
# Type: method
# Description: Helper method to setup auth parameters for RPC calls
# End-Doc


def login(username, password):
    global rpc_auth_user, rpc_auth_pass
    rpc_auth_user = username
    rpc_auth_pass = password

# Begin-Doc
# Name: rpc
# Type: method
# Description: Helper method to setup RPC connection for calls
# End-Doc


def rpc():
    global netgroup_rpc, rpc_auth_pass, rpc_auth_user
    if netgroup_rpc is not None:
        return netgroup_rpc

    host = "https://itrpc-groups-dev.mst.edu"
    env = local_env()

    if env == "test":
        host = "https://itrpc-groups-test.mst.edu"
    elif env == "prod":
        host = "https://itrpc-groups.mst.edu"

    netgroup_rpc = SimpleRPCClient(
        base_url=f"{host}/auth-perl-bin/UserGroup",
        username=rpc_auth_user,
        password=rpc_auth_pass
    )

    return netgroup_rpc

# Begin-Doc
# Name: exists
# Type: method
# Description: returns true if user netgroup exists
# Syntax: res = netgroup.exists(groupname)
# End-Doc


@ttl_cache(DEFAULT_TTL)
def exists(group, actor=None):
    res = rpc().Exists(group=group, actor=actor)
    return group in res[0] and res[0][group] == 1

# Begin-Doc
# Name: list
# Type: method
# Description: returns list of user netgroups
# Syntax: groups = netgroup.list()
# End-Doc


@ttl_cache(DEFAULT_TTL)
def list(actor=None):
    info = rpc().List(actor=actor)
    return info[0]

# Begin-Doc
# Name: member_users
# Type: method
# Description: returns list of that are members of group
# Syntax: members = netgroup.member_users(group)
# End-Doc


@ttl_cache(DEFAULT_TTL)
def member_users(group, actor=None):
    res = rpc().MemberUsers(group=group, actor=actor)
    return res[0][group]
