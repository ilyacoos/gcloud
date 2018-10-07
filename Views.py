'''
Created on 7 окт. 2018 г.

@author: 16704132
'''

class FullScreenAll(object):
    '''
    Line chart, show fullscreen all series
    '''


    def __init__(self, table):
        '''
        table - table to visualise
        '''
        self.table = table
    
    def show(self):
        out = """<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([["""
        for col in self.table[0]:
            out = out + "'%s'," % col
        out = out + "]"
        
        for row in self.table[1:]:
            out = out + ",[new Date(%d)" % row[0]
            for cel in row[1:]:
                out = out + ", %f" % cel
            out = out + "]"
        out = out + """ ]);

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
</html>"""
        return out