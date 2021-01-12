# Begin-Doc
# Name: db.py
# Type: package
# Description: Implements MySQLObject class
# End-Doc

from mstpylib import local_env, authsrv
import re
import getpass
import mysql.connector

HOSTS = {
    "sysd": "sysdb-dev.srv.mst.edu",
    "syst": "sysdb-test.srv.mst.edu",
    "sysp": "sysdb.srv.mst.edu"
}

WAIT_TIMEOUT = 300

shared_connections = {}
shared_counts = {}

# Begin-Doc
# Name: MySQLObject
# Type: class
# Description: Wrapper around mysql-connector-python package to implement similar behavior to Perl MST::MySQLObject
# End-Doc


class MySQLObject:

    # Begin-Doc
    # Name: __init__
    # Type: method
    # Description: Initialize MySQLObject
    # End-Doc
    def __init__(self):
        self.conn = None
        self.host = None
        self.user = None
        self.database = None
        self.shared = False
        self.wait_timeout = WAIT_TIMEOUT

    # Begin-Doc
    # Name: __hash__
    # Type: method
    # Description: provide a mechanism for hashing MySQLObjects as keys in dictionaries
    # End-Doc
    def __hash__(self):
        return hash((self.host, self.user, self.database))

    # Begin-Doc
    # Name: __eq__
    # Type: method
    # Description: provide a mechanism for determining whether two MySQLObjects are equivalent
    # End-Doc
    def __eq__(self, other):
        return (self.host, self.user, self.database) == (other.host, other.user, other.database)

    # Begin-Doc
    # Name: __set_session__
    # Type: method
    # Description: set pre-defined session variables upon connection/reconnection
    # End-Doc
    def __set_session__(self):
        self.SQL_ExecQuery("SET SESSION wait_timeout=%s", [self.wait_timeout])

    # Begin-Doc
    # Name: __reconnect__
    # Type: method
    # Description: internal method used to reconnect to mysql and set necessary session variables
    # End-Doc
    def __reconnect__(self):
        self.conn.reconnect()
        self.__set_session__()

    # Begin-Doc
    # Name: SQL_OpenDatabase
    # Type: method
    # Description: connects to specificed mysql host/database
    #   leverage sysd/syst/sysp/sys* shorthand notation
    # End-Doc
    def SQL_OpenDatabase(self, host, user=None, passwd=None, database=None, shared_pooling=True, wait_timeout=WAIT_TIMEOUT):
        global HOSTS
        target_host = None


        if host in HOSTS:
            target_host = HOSTS[host]
        else:
            match = re.search("^(.*)\*$", host)
            if match is not None:
                suffix = "d"
                suffixes = {
                    "dev": "d",
                    "test": "t",
                    "prod": "p"
                }

                if local_env() in suffixes:
                    suffix = suffixes[local_env()]

                target_host = HOSTS[f"{match.group(1)}{suffix}"]
            else:
                target_host = host

        if user is None:
            user = getpass.getuser()

            if database is None:
                database = user

        if passwd is None:
            passwd = authsrv.fetch(user=user, instance="mysql")

        if self.conn is not None:
            self.SQL_CloseDatabase()

        self.host = target_host
        self.user = user
        self.database = database
        self.shared = shared_pooling
        self.wait_timeout = wait_timeout

        if shared_pooling and self in shared_connections:
            shared_counts[self] += 1
            self.conn = shared_connections[self]
            return shared_connections[self]
        else:
            self.conn = mysql.connector.connect(
                host=target_host, user=user, password=passwd, database=database, autocommit=True)
            self.__set_session__()

        if shared_pooling:
            shared_connections[self] = self.conn
            shared_counts[self] = 1

        return self.conn

    # Begin-Doc
    # Name: SQL_CloseDatabase
    # Type: method
    # Description: closes active connection to mysql
    # End-Doc
    def SQL_CloseDatabase(self):
        if self.conn is not None:
            if self.shared and self in shared_counts:
                if shared_counts[self] > 1:
                    shared_counts[self] -= 1
                else:
                    self.conn.close()
                    self.conn = None
            else:
                self.conn.close()
                self.conn = None

    # Begin-Doc
    # Name: SQL_AutoCommit
    # Type: method
    # Description: turns on/off autocommit
    # End-Doc
    def SQL_AutoCommit(self, val):
        if not self.conn.is_connected():
            self.__reconnect__()
        self.conn.autocommit = val

    # Begin-Doc
    # Name: SQL_Commit
    # Type: method
    # Description: commits a transaction
    # End-Doc
    def SQL_Commit(self):
        if not self.conn.is_connected():
            self.__reconnect__()
        self.conn.commit()

    # Begin-Doc
    # Name: SQL_ExecQuery
    # Type: method
    # Description: Executes a SQL query
    # End-Doc
    def SQL_ExecQuery(self, query, params=None):
        if not self.conn.is_connected():
            self.__reconnect__()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        cursor.close()

    # Begin-Doc
    # Name: SQL_OpenQuery
    # Type: method
    # Descriptions: Opens a cursor to a query
    # End-Doc
    def SQL_OpenQuery(self, query, params=None):
        if not self.conn.is_connected():
            self.__reconnect__()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    # Begin-Doc
    # Name: SQL_CloseQuery
    # Type: method
    # Description: Closes cursor to an open query
    # End-Doc
    def SQL_CloseQuery(self, cursor):
        cursor.close()

    # Begin-Doc
    # Name: SQL_FetchRow
    # Type: method
    # Description: Grabs a single tuple from an open cursor
    # End-Doc
    def SQL_FetchRow(self, cursor):
        return cursor.fetchone()

    # Begin-Doc
    # Name: SQL_FetchRow_LowerDict
    # Type: method
    # Description: Grabs a single row from an open cursor defined on key/value pairs of column_name/column_value
    # End-Doc
    def SQL_FetchRow_LowerDict(self, cursor):
        cols = self.SQL_LowerColumns(cursor)
        if vals := self.SQL_FetchRow(cursor):
            return dict(zip(cols, vals))

    # Begin-Doc
    # Name: SQL_LowerColumns
    # Type: method
    # Description: Returns tuple of column names of an open cursor, all lowercase
    # End-Doc
    def SQL_LowerColumns(self, cursor):
        return [x.lower() for x in cursor.column_names]
