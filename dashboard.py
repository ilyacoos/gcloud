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
    main = webapp2.WSGIApplication([
        ('/a3/stat', Stat)
    ], debug=True)

except Exception as e:
    class DefPage(webapp2.RequestHandler):
        def get(self):self.response.write("<html><body>Web-site is under development.</body></htnl><!--\n%s\n-->" % e.message)
    main = webapp2.WSGIApplication([('.*', DefPage)], debug=True)
