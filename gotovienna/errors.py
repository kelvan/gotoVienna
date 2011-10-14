class LineNotFoundError(Exception):
    def __init__(self, msg="Unknown line"):
        self.message = msg
        
    def __str__(self):
        return self.message
    
class StationNotFoundError(Exception):
    def __init__(self, msg="Unknown station"):
        self.message = msg
        
    def __str__(self):
        return self.message