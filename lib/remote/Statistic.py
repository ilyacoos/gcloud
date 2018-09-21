import cgi
import webapp2
import Database

class Statistic(webapp2.RequestHandler):
    def get(self):
        _req = self.request.get('req')
        if _req:
            pass
            """"O = Database.Database()
            O.connect()
            rec = O.query(_req)
            self.response.write("<html><body>")
            
            if rec[0] == Database.RECORDSET:
                for col in rec[2]: self.response.write("<tr><th>%s</th></tr>" % col)
                for row in rec[3]:
                    for col in row: self.response.write("<tr><td>%s</td></tr>" % col)
            if rec[0] == Database.ERROR:
                self.response.write("Error. <!--%s-->" % rec[1])
            if rec[0] == Database.STATEMENT:
                self.response.write("Completed:<br />%s" % _req)
            O.close()
            self.response.write("</body></html>")"""
