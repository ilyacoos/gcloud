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

class Torrent(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    url = ndb.TextProperty(required=True)
    tgt = ndb.TextProperty(required=True)
    added = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.IntegerProperty(indexed=True, required=True, default=STATUS_NEW)
    finished = ndb.DateTimeProperty(auto_now_add=False)


class AddTorrent(webapp2.RequestHandler):
    def get(self):
        try:
            if self.request.get('pswd') != APP_PSWD: raise Exception
            name = self.request.get('name')
            url = self.request.get('url')
            tgt = self.request.get('tgt')
            if name and url and tgt:
                torrent = Torrent(
                    name = self.request.get('name'),
                    url = self.request.get('url'),
                    tgt = self.request.get('tgt'))
                torrent.put()
            else:
                raise Exception
        except:
            self.response.write(RESPONSE_ERR)
        else:
            self.response.write(RESPONSE_OK)

class SetStat(webapp2.RequestHandler):
    def get(self):
        try:
            if self.request.get('pswd') != APP_PSWD: raise Exception
            name = self.request.get('name')
            status = self.request.get('status')
            if name and status:
                torrent = Torrent.query(Torrent.name == name).get()
                torrent.status = int(status)
                torrent.put()
            else:
                raise Exception
        except:
            self.response.write(RESPONSE_ERR)
        else:
            self.response.write(RESPONSE_OK)

class GetStat(webapp2.RequestHandler):
    def get(self):
        try:
            if self.request.get('pswd') != APP_PSWD: raise Exception
            name = self.request.get('name')
            if name:
                torrent = Torrent.query(Torrent.name == name).get()
                if not torrent: raise Exception
            else:
                raise Exception
        except:
            self.response.write(RESPONSE_ERR)
        else:
            self.response.write(torrent.status)

class List(webapp2.RequestHandler):
    def get(self):
        try:
            if self.request.get('pswd') != APP_PSWD: raise Exception
            if self.request.get('new'):
                list = Torrent.query(Torrent.status == STATUS_NEW).fetch(100)
            else:
                list = Torrent.query().fetch(100)
        except:
            self.response.write(RESPONSE_ERR)
        else:
            for torrent in list:
                self.response.write('"%s"   "%s"    "%s" %i\n' % (torrent.name, torrent.url, torrent.tgt, torrent.status) )

class Pending(webapp2.RequestHandler):
    def get(self):
        try:
            if self.request.get('pswd') != APP_PSWD: raise Exception
            l = len( Torrent.query(Torrent.status == STATUS_NEW).fetch(100) )
            if l == 0: raise Exception
        except:
            self.response.write(RESPONSE_ERR)
        else:
            self.response.write( l )

class KillTorrent(webapp2.RequestHandler):
    def get(self):
        try:
            if self.request.get('pswd') != APP_PSWD: raise Exception
            name = self.request.get('name')
            if name:
                Torrent.query(Torrent.name == name).get().key.delete()
        except:
            self.response.write(RESPONSE_ERR)
        else:
            self.response.write(RESPONSE_OK)

