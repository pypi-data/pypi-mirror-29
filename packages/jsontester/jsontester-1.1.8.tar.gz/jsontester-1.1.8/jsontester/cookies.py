"""
Read cookies from chrome browser cookies
"""

import sys
import os
import configobj

from requests import cookies
from .sqlite import SQLiteDatabase

# Cookie paths:
# ~/Library/Application Support/Firefox/Profiles/toxwdvmv.default/cookies.sqlite
# ~/.firefox/Profiles/toxwdvmv.default/cookies.sqlite

class CookieError(Exception):
    pass


if sys.platform=='darwin':
    CHROME_CONFIG_DIR = os.path.join(
        os.getenv('HOME'), 'Library', 'Application Support', 'Google', 'Chrome', 'Default'
    )
    FIREFOX_CONFIG_DIR = os.path.join(
        os.getenv('HOME'), 'Library', 'Application Support', 'Firefox'
    )
elif sys.platform in [ 'linux', 'linux2', 'freebsd9']:
    CHROME_CONFIG_DIR = os.path.expanduser('~/.config/chromium/Default')
    FIREFOX_CONFIG_DIR = os.path.expanduser('~/.mozilla/firefox')
else:
    CHROME_CONFIG_DIR = None
    FIREFOX_CONFIG_DIR = None


class BrowserSQLiteCookies(SQLiteDatabase):
    def __init__(self, browser, path):
        self.name = browser
        SQLiteDatabase.__init__(self, path)


class FirefoxCookies(BrowserSQLiteCookies):
    def __init__(self, name='firefox', configdir=None):
        self.configdir = configdir and configdir or FIREFOX_CONFIG_DIR
        if self.configdir is None:
            raise CookieError('Could not find {0} configuration directory'.format(name))
        if not os.path.isdir(self.configdir):
            raise CookieError('No such directory: {0}'.format(self.configdir))
        profile_path = self.get_profile_path()
        if profile_path is None:
            raise CookieError('Could not find {0} profile directory'.format(name))
        path = os.path.join(self.configdir, profile_path, 'cookies.sqlite')
        BrowserSQLiteCookies.__init__(self, name, path)

    def get_profile_path(self, name='default'):
        config = configobj.ConfigObj(os.path.join(self.configdir, 'profiles.ini'))
        for section, items in config.items():
            if section[:7] != 'Profile' or 'Name' not in items:
                continue
            if items['Name'] == name:
                return items['Path']
        return None

    def lookup(self, host, name=None):
        c = self.cursor
        c.execute('select host, name, value from moz_cookies')

        if name is not None:
            c.execute("""SELECT name, value FROM moz_cookies WHERE host=? AND name=?""", (host, name,))
        else:
            c.execute("""SELECT name, value FROM moz_cookies WHERE host=?""", (host,))

        cookies = dict((c[0],c[1]) for c in c.fetchall())
        self.log.debug('{0} cookies for host {1}: {2}'.format(self.name, host, cookies))
        return cookies


class ChromeCookies(BrowserSQLiteCookies):
    def __init__(self, name='chrome', configdir=None):
        self.configdir = configdir and configdir or CHROME_CONFIG_DIR
        if self.configdir is None:
            raise CookieError('Could not find {0} configuration directory'.format(name))
        if not os.path.isdir(self.configdir):
            raise CookieError('No such directory: {0}'.format(self.configdir))
        path = os.path.join(self.configdir, 'Cookies')
        BrowserSQLiteCookies.__init__(self, name, path)

    def lookup(self, host, name=None):
        c = self.cursor
        if name is not None:
            c.execute("""SELECT name, value FROM cookies WHERE host_key=? AND name=?""", (host, name,))
        else:
            c.execute("""SELECT name, value FROM cookies WHERE host_key=?""", (host,))

        cookies = dict((c[0], c[1]) for c in c.fetchall())
        self.log.debug('{0} cookies for host {1}: {2}'.format(self.name, host, cookies))
        return cookies


def get_host_cookies(browser, host, name=None):
    if browser == 'firefox':
        cookies = FirefoxCookies(name=browser)
    elif browser in ['chrome', 'chromium']:
        cookies = ChromeCookies(name=browser)
    else:
        raise CookieError('Unknown browser: {0}'.format(browser))
    return cookies.lookup(host, name)

