#import cgi
import webapp2

class Stat(webapp2.RequestHandler):
    def get(self):
        try:
            import sys
            sys.path.insert(0, 'lib')
            from bs4 import BeautifulSoup
            from urllib2 import urlopen
            

            HTML = urlopen("http://pif.investfunds.ru/funds/54/detail/1/", data="date1    01.01.2018\ndate2    20.09.2018\nset_compare[5]    0").read()
            soup = BeautifulSoup(HTML)
            table = soup.find("div", attrs={"class":"tabs-inner tabs-inner-active"}).find_all("table", attrs={"class":"table-data"})[1].find_all("tr")
            self.response.write("<html><body>")
            self.response.write("<!--" + table + "-->")
            for r in table:
                self.response.write("%s, %s, %s <br />" % r.find_all("td"))
                
            self.response.write("</body></html>")

        except Exception as e:
            self.response.write(e.message)

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
        ('/a2/stat', Stat),
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
