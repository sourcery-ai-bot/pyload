# -*- coding: utf-8 -*-

import time

from module.plugins.internal.Account import Account
from module.plugins.internal.misc import json


class FileserveCom(Account):
    __name__    = "FileserveCom"
    __type__    = "account"
    __version__ = "0.26"
    __status__  = "testing"

    __description__ = """Fileserve.com account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("mkaay", "mkaay@mkaay.de")]


    def grab_info(self, user, password, data):
        html = self.load("http://app.fileserve.com/api/login/",
                         post={'username': user,
                               'password': password,
                               'submit': "Submit+Query"})
        res = json.loads(html)

        if res['type'] != "premium":
            return {'premium': False, 'trafficleft': None, 'validuntil': None}

        validuntil = time.mktime(time.strptime(res['expireTime'], "%Y-%m-%d %H:%M:%S"))
        return {'trafficleft': res['traffic'], 'validuntil': validuntil}


    def signin(self, user, password, data):
        html = self.load("http://app.fileserve.com/api/login/",
                         post={'username': user,
                               'password': password,
                               'submit'  : "Submit+Query"})
        res = json.loads(html)

        if not res['type']:
            self.fail_login()

        #: Login at fileserv html
        self.load("http://www.fileserve.com/login.php",
                  post={'loginUserName'    : user,
                        'loginUserPassword': password,
                        'autoLogin'        : "checked",
                        'loginFormSubmit'  : "Login"})
