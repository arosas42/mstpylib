# Begin-Doc
# Name: mysql.py
# Type: package
# Description: wrapper package around sqlalchemy.create_engine to leverage authsrv (think SQL_OpenDatabase("sal*"))
# End-Doc
from mstpylib import authsrv, local_env, setuid
from sqlalchemy import create_engine as ce
import re
import getpass

HOSTS = {
    "sysd": "sysdb-dev.srv.mst.edu",
    "syst": "sysdb-test.srv.mst.edu",
    "sysp": "sysdb.srv.mst.edu",
}

# Begin-Doc
# Name: create_engine
# Type: method
# Description: wrapper method around sqlalchemy.create_engine to leverage authsrv (think SQL_OpenDatabase("sys*"))
# End-Doc
def create_engine(host, **kwargs):
    global HOSTS
    target_host = None
    env = local_env()
    uri = None

    if host in HOSTS:
        target_host = HOSTS[host]
    elif match := re.search("^(.*)\*$", host):
        suffix = "d"
        suffixes = {
            "dev": "d",
            "test": "t",
            "prod": "p"
        }

        if env in suffixes:
            suffix = suffixes[env]

        envhost = f"{match.group(1)}{suffix}"
        if envhost in HOSTS:
            target_host = HOSTS[envhost]

    if target_host is None:
        uri = host
    else:
        user = kwargs.get("user", getpass.getuser())
        passwd = kwargs.get(
            "passwd",
            authsrv.fetch(user=user, instance="mysql")
        )
        database = kwargs.get("database", user)
        uri = f"mysql+pymysql://{user}:{passwd}@{target_host}/{database}"
    args = kwargs.get("connect_args")
    if args is not None:
        return ce(uri, connect_args=args)
    else:
        return ce(uri)