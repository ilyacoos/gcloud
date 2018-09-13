#import cgi
import webapp2


try:
    import sys
    sys.path.insert(0, 'lib')
    from remote.Pif import PifApp
    from remote.Help import MainPage,Req
    from remote.Statistic import Statistic
    from remote.Remote import (
        AddTorrent,
        SetStat,
        GetStat,
        List,
        KillTorrent,
        Pending )
    
    a2 = webapp2.WSGIApplication([
        ('/a2/pif', PifApp),
        ('/a2/help', MainPage),
        ('/a2/req', Req),
        ('/a2/torrent/add', AddTorrent),
        ('/a2/torrent/set_stat', SetStat),
        ('/a2/torrent/get_stat', GetStat),
        ('/a2/torrent/list', List),
        ('/a2/torrent/kill', KillTorrent),
        ('/a2/torrent/pending', Pending),
        ('/a2/stat', Statistic)
    ], debug=True)

except Exception as e:
    class DefPage(webapp2.RequestHandler):
        def get(self):self.response.write("<html><body>Web-site is under development.</body></htnl><!--\n%s\n-->" % e.message)
    a2 = webapp2.WSGIApplication([('.*', DefPage)], debug=True)
