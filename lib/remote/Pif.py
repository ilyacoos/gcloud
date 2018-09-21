import cgi
import urllib

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

import webapp2



class PifList(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    symbol = ndb.StringProperty(required=True)
    url = ndb.TextProperty(required=True)


class PifApp(webapp2.RequestHandler):
    def get(self):
        try:
            from bs4 import BeautifulSoup
            from urllib2 import urlopen
            # Shares
            pifs = PifList.query().fetch(1000)
            if len(pifs) == 0: return
            
            dataset = []
            for pif in pifs:
                try:
                    HTML = urlopen(pif.url).read()
                    soup = BeautifulSoup(HTML)
                    table = soup.find("table", attrs={"class":"tbl-column2"}).find("table", attrs={"class":"table-data"})
                    date = table.find_all("tr")[1].find_all("td")[1].get_text()
                    value = table.find_all("tr")[2].find_all("td")[1].get_text().replace(" ", "")
                    dataset.append( (date, pif.name, pif.symbol, value, pif.url) )
                except:
                    pass
        except Exception as e:
            self.response.write(e.message)
        else:
            self.response.write("<html><head><title>PIFs Statistics 100</title></head><body><table><tr><th>Date</th><th>Name</th><th>Symbol</th><th>Value</th></tr>")
            for row in dataset:
                self.response.write('<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>' % (row[0], row[4], row[1], row[2], row[3]) )
            self.response.write("</table></body></html>")