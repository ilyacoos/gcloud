'''
Created on 24 сент. 2018 г.

@author: 16704132
'''

import sys
sys.path.insert(0, 'lib')


def testURL():
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    #HTML = urlopen("http://pif.investfunds.ru/funds/54/detail/1/", data=bytes("date1    01.01.2018\ndate2    20.09.2018\nset_compare[5]    0", 'utf-8') ).read()
    HTML = urlopen("http://pif.investfunds.ru/funds/54/detail/1/?&day1=01&month1=12&year1=2017&day2=21&month2=09&year2=2018&date1=01.12.2017&date2=21.09.2018&start=90&rand=0.6264447805138752#beginf").read()
    soup = BeautifulSoup(HTML, "lxml")
    table = [[c.get_text().replace(" ", "") for c in r.find_all("td")] for r in soup.find("div", attrs={"class":"tabs-inner tabs-inner-active"}).find_all("table", attrs={"class":"table-data"})[1].find_all("tr")]
    print(table[0] [:])
    
    for r in table[1:]:
        r[0] = "new Date('%s')" % (r[0].replace(".", "-"))
                                   
    table[0] = ["Data", "Pie", "Volume"]
    
    print ("""
  <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([['Data', 'Pie', 'Volume']""")
    for r in  table[1:]: 
        print( ",[%s, %s, %s]" % (r[0], r[1], r[2]) )
      
    print("""]);

        var options = {
          title: 'Company Performance',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="curve_chart" style="width: 900px; height: 500px"></div>
  </body>
</html>
    """ % table)
        
    #for r in table:
    #    print("%s, %s, %s <br />" % r.find_all("td"))
        

    

def testTest(p):
    """from Crowler import Crowler
    c = Crowler("http://pif.investfunds.ru/funds/54/detail/1/?&day1=01&month1=12&year1=2017&day2=21&month2=09&year2=2018&date1=01.12.2017&date2=21.09.2018&start=90&rand=0.6264447805138752#beginf",
                [["div", {"class":"tabs-inner tabs-inner-active"}], ["table", {"class":"table-data"}, 1], ["tr", None, [1, None]] ],
                [ ["td",None,0], ["td",None,1], ["td",None,2] ]
                 )
    
    print ( c.get() )
    """
    from Crowler import Crowler
    from Views import FullScreenAll as FSA
    c = Crowler("investfunds.pif", {"fund": 1003})
    
    o = c.get("01.07.2018", "04.10.2018")
    
    tbl = [['Data', 'Pie', 'Users']]
    for r in o.keys():
        # print( ",[new Date(%d), %f, %f]" % (r, o[r]["share"], o[r]["volume"]/o[r]["share"]/1000000) )
        tbl.append([r, o[r]["share"], o[r]["volume"]/o[r]["share"]/2000000])
    
    out = FSA(tbl)
    print (out.show())
    
if __name__ == '__main__':
    testTest([0,0])
