import cgi
import urllib

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

import webapp2



HELP_HTML = """<html><body>
<ul><li>/torrent/add<ul><li>name - Torrent name</li><li>url - source URL</li><li>tgt - Target folder</li><li>pswd - App.password</li></ul></li></ul>
<ul><li>/torrent/set_stat<ul><li>name - Torrent name</li><li>status - Status to set</li><li>pswd - App.password</li></ul></li></ul>
<ul><li>/torrent/get_stat<ul><li>name - Torrent name</li><li>pswd - App.password</li></ul></li></ul>
<ul><li>/torrent/list<ul><li>new - Show only status -1 records (any value)</li><li>pswd - App.password</li></ul></li></ul>
<ul><li>/torrent/pending<ul><li>pswd - App.password</li></ul></li></ul>
<ul><li>/torrent/kill<ul><li>name - Torrent name</li><li>pswd - App.password</li></ul></li></ul>
<hr><a href="%s">Logout</a></body></html>"""

APP_PSWD = '1'
APP_OWNER = 'grigoryev.ilya.l@gmail.com'
DEFAULT_CONTROLS_NAME = 'default_controls'
RESPONSE_OK = 'OK'
RESPONSE_ERR = 'Error'
STATUS_NEW = -1


def control_key(section_name='Torrent', entry_name=DEFAULT_CONTROLS_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key(section_name, entry_name)


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and user.email() == APP_OWNER:
            self.response.write(HELP_HTML % users.create_logout_url(self.request.uri) )
        else:
            self.response.write('<html><body><a href="%s">Login</a></body></html>' % users.create_login_url(self.request.uri) )

class Req(webapp2.RequestHandler):
    def get(self):
        self.response.write( dir(self.request.get) )