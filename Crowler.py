'''
Created on 7 окт. 2018 г.

@author: 16704132
'''

class Crowler(object):
    '''
    Crowler: Data-provider/Parser -> get(Date range) -> Table-data
    '''

    def __init__(self, parser, attrs):
        '''
        parser, attrs - specific parser for a data-rovider and his specfic attributes
            - "investfunds.pif": {fund: fundID}
            - "general"
        '''
        if parser == "investfunds.pif":
            self.parser = self.__Investfunds_pifs(attrs)
        elif parser == "general":
            self.parser = self.__General(attrs)
        else:
            help(self)
            raise ValueError("Error: Parser not found")
            

    def get(self, startDt, endDt):
        return self.parser.get(startDt, endDt)


    class __Investfunds_pifs(object):
        def __init__(self, attrs):
            self.attrs = attrs
        
        def get(self, startDt, endDt):
            from bs4 import BeautifulSoup
            from urllib.request import urlopen
            from datetime import datetime
            
            html = urlopen("http://pif.investfunds.ru/quotes/",
                           data = bytes("lastdate2=%s&lastdate=%s&type[]=открытый&type[]=интервальный&type[]=закрытый&category_id=&value=&c_val[1]=0&c_val[4]=0&c_val[2]=0&c_val[5]=0&fund_name=&f1[]=%s&f2[]=%s&rtable=1&export_type=&what=1&rel=1" % (startDt, endDt, self.attrs["fund"], self.attrs["fund"] ), "UTF8") ).read()
            dom  = BeautifulSoup(html, "lxml")
            
            table = [[c.get_text() for c in r.find_all("td")] for r in dom.find("div", attrs={"class":"tabs-container"}).find("table", attrs={"class":"table-data"}).find_all("tr")[2:] ]
            
            out={}
            gmt = datetime(1970,1,1)
            for r in table:
                key = (datetime.strptime(r[0], "%d.%m.%Y") - gmt).days * 3600 * 24 * 1000 - 3 * 3600 * 1000
                out[key] = {"share": float(r[1].replace(" ", "")), "volume": float(r[2].replace(" ", "")) }
            return out
            #dict(reversed(table))

    class __General(object):
        
        def __init__(self, attrs):
            self.attrs = attrs
        
        def get(self):
            from bs4 import BeautifulSoup
            from urllib.request import urlopen
            
            
            
            if self.paging:
                doc = BeautifulSoup(urlopen(self.url % 0*self.paging[0]).read(), "lxml")
                docS = doc
                for node in self.paging[1:]:
                    if len(node) == 2:
                        docS = docS.find(node[0], attrs=node[1])
                    elif isinstance(node[2], int):
                        docS = docS.find_all(node[0], attrs = node[1])[node[2]]
                    else:
                        docS = docS.find_all(node[0], attrs = node[1])[node[2][0] : node[2][1]]
                pages = len(docS)
            else:
                doc = BeautifulSoup(urlopen(self.url).read(), "lxml")
                pages = [1]
            
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