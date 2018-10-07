'''
Created on 7 окт. 2018 г.

@author: 16704132
'''

class Crowler(object):
    
    '''
    Crowler: URL -> HTML-parser -> JSON-data
    '''


    def __init__(self, url, data, table):
        '''
        url - extract page
        data - structure to extract [ [tag, attrs@jsoup, multiplicatility = None|Int|Interval], ... ]
        
        '''
        self.url = url
        self.data = data
        self.table = table
        
    def get(self):
        from bs4 import BeautifulSoup
        from urllib.request import urlopen
        
        doc = BeautifulSoup(urlopen(self.url).read(), "lxml")
        
        for node in self.data:
            if len(node) == 2:
                doc = doc.find(node[0], attrs=node[1])
            elif isinstance(node[2], int):
                doc = doc.find_all(node[0], attrs = node[1])[node[2]]
            else:
                doc = doc.find_all(node[0], attrs = node[1])[node[2][0] : node[2][1]]
        
        ret = []
        for row in doc:
            retR = []
            for cell in self.table:
                retR.append( row.find_all(cell[0], attrs=cell[1])[cell[2]].get_text().replace(" ", "") )
            ret.append(retR)
        
        return ret
            
        # table = [[c.get_text().replace(" ", "") for c in r.find_all("td")] for r in soup.find("div", attrs={"class":"tabs-inner tabs-inner-active"}).find_all("table", attrs={"class":"table-data"})[1].find_all("tr")]
    
    