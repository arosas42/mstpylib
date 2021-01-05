# Begin-Doc
# Name: simplerpc.py
# Type: package
# Description: implements the SimpleRPCClient class to manage our simplified RPC implementation
# End-Doc
import urllib.request
import urllib.parse
import json
import base64

# Begin-Doc
# Name: SimpleRPCClient
# Type: class
# Description: Client object to interface with our simplified RPC servers
# End-Doc


class SimpleRPCClient:

    # Begin-Doc
    # Name: __getattr__
    # Type: method
    # Description: internal python magic method that gets called when __getattribute__ fails to find named attribute
    #  used to overload unnamed functions as calls to CallRPC() method
    # End-Doc
    def __getattr__(self, name):
        def func(*args, **kwargs):
            return self.CallRPC(name, *args, **kwargs)
        return func

    # Begin-Doc
    # Name: __init__
    # Type: method
    # Description: instantiates new SimpleRPCClient object
    # End-Doc
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.username = username
        self.password = password

    # Begin-Doc
    # Name: _headers
    # Type: method
    # Description: internal method used to inject HTTP headers into RPC calls (specifically for basic auth when needed)
    # End-Doc
    def _headers(self):
        headers = {"User-Agent": "mstpylib/SimpleRPCClient:v1.0"}
        if self.username is not None and self.password is not None:
            basic_auth = base64.encodestring(
                f"{self.username}:{self.password}")
            headers["Authentication"] = f"Basic {basic_auth}"
        return headers

    # Begin-Doc
    # Name: CallRPC
    # Type: method
    # Description: worker method that implements the RPC operation
    # End-Doc
    def CallRPC(self, name, args=None):
        url = f"{self.base_url}/{name}"
        data = None
        if args is not None:
            data = urllib.parse.urlencode(args).encode()
        req = urllib.request.Request(
            url=url, headers=self._headers(), data=data, method="POST")
        resp = urllib.request.urlopen(req)

        val, msg, *data = json.loads(resp.read())

        if val != 0:
            raise Exception(f"Error returned from RPC: {msg}")

        return data
