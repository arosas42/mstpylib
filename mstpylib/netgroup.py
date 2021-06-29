# Begin-Doc
# Name: netgroup.py
# Type: package
# Description: Package/wrapper around Netgroup RPC calls
# End-Doc
from mstpylib.simplerpc import SimpleRPCClient
from mstpylib.usage_logger import LogAPIUsage
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
    LogAPIUsage()

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
    LogAPIUsage()

    [res] = rpc().Exists(group=group, actor=actor)
    return group in res and res[group] == 1

# Begin-Doc
# Name: list
# Type: method
# Description: returns list of user netgroups
# Syntax: groups = netgroup.list()
# End-Doc


@ttl_cache(DEFAULT_TTL)
def list(actor=None):
    LogAPIUsage()

    [info] = rpc().List(actor=actor)
    return info

# Begin-Doc
# Name: member_users
# Type: method
# Description: returns list of that are members of group
# Syntax: members = netgroup.member_users(group)
# End-Doc


@ttl_cache(DEFAULT_TTL)
def member_users(group, actor=None):
    LogAPIUsage()

    [res] = rpc().MemberUsers(group=group, actor=actor)
    return res[group]


# Begin-Doc
# Name: member_users_multi
# Type: method
# Description: Returns dictionary of users that are members of each group
# Syntax: members_by_group = netgroup.member_users_multi(group1, group2, ...)
# End-Doc

@ttl_cache(DEFAULT_TTL)
def member_users_multi(*args, actor=None):
    LogAPIUsage()

    [res] = rpc().MemberUsers(group=args, actor=actor)
    return res