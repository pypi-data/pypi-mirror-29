"""
    This module does tricks to hide private and protected members
    from PyCharms intellisense.

    Import from here if you want a reduced intellisense.

    This is based on:
        http://stackoverflow.com/questions/23457532/
        in-python-can-i-hide-a-base-class-members

"""

from seaborn.request_client import endpoint
from seaborn.request_client import connection_basic
from seaborn.request_client import connection_endpoint

from .repr_wrapper import repr_return


class Endpoint(endpoint.Endpoint):
    pass


class ConnectionBasic(connection_basic.ConnectionBasic):
    def __init__(self, username=None, password=None, login_url=None,
                 auth_url=None, api_key=None, base_uri=None,
                 proxies=None, timeout=None, headers=None,
                 cookies=None, accepted_return=None):
        """
        :param username        : str of user's email to use for the session.
        :param password        : str of password for the user
        :param login_url       : str of the login_url to auto login to
        :param auth_url        : str of the auth_url, if Oauth2 is used
        :param api_key         : str of api key of the client software
        :param base_uri        : str of base url
        :param proxies         : str of proxies dictionary as used in requests
        :param timeout         : str of timeout to use for api call
        :param headers         : str of specially header to use for api calls
        :param cookies         : list of cookies to use in the http request
        :param accepted_return : str of enum ['json','text','html']
        """
        super(ConnectionBasic, self).__init__(username, password, login_url,
                                              auth_url, api_key, base_uri,
                                              proxies, timeout, headers,
                                              cookies, accepted_return)

    def login(self, username=None, password=None, login_url=None,
              auth_url=None):
        """
        This will automatically log the user into the pre-defined account

        Feel free to overwrite this with an endpoint on endpoint load

        :param username:  str of the user name to login in as
        :param password:  str of the password to login as
        :param login_url: str of the url for the server's login
        :param auth_url:  str of the url for the server's authorization login
        :return: str of self._status
        """
        return super(ConnectionBasic, self).login(username, password,
                                                  login_url, auth_url)


class ConnectionEndpoint(connection_endpoint.ConnectionEndpoint,
                         ConnectionBasic):
    def __init__(self, username=None, password=None, login_url=None,
                 auth_url=None, api_key=None, base_uri=None,
                 proxies=None, timeout=None, headers=None, cookies=None,
                 accepted_return=None):
        """
        :param username        : str of user's email to use for the session.
        :param password        : str of password for the user
        :param login_url       : str of the login_url to auto login too
        :param auth_url        : str of the auth_url, if Oauth2 is used
        :param api_key         : str of api key of the client software
        :param base_uri        : str of base url
        :param proxies         : str of proxies dictionary as used in requests
        :param timeout         : str of timeout to use for api call
        :param headers         : str of specially header to use for api calls
        :param cookies         : list of cookies to use in the http request
        :param accepted_return : str of enum ['json','text','html']
        """
        super(ConnectionEndpoint, self).__init__(username, password, login_url,
                                                 auth_url, api_key, base_uri,
                                                 proxies, timeout, headers,
                                                 cookies, accepted_return)

    @property
    @repr_return
    def api_tree(self):
        return self._create_tree()
