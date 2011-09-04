from BeautifulSoup import BeautifulSoup

class ParserError(Exception):
     def __init__(self, value='', code=0):
         self.value = value
         self.code = code

     def __str__(self):
         return repr(self.value)

class cParser:

    def __init__(self, html):
        self.soup = BeautifulSoup(html)
        
    def find_options(self):
        nlo = self.soup.find('select', {'id': 'nameList_origin'})
        nld = self.soup.find('select', {'id': 'nameList_destination'})
        
        if not nlo or not nld:
            raise ParserError('Unable to parse html')
        
        origin = nlo.findAll('option')
        destination = nld.findAll('option')
        
        if not origin:
            origin = []
        if not destination:
            destination = []
        
        return (origin, destination)