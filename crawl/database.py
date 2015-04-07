class Database(object):
    """docstring for Database"""
    def __init__(self, dbname='database'):
        super(Database, self).__init__()
        self.dbName = dbname + ".db"
        self._size = 0
    
    def openDb(self):
        self.file = open(self.dbName, 'a+')
    
    def closeDb(self):
        self.file.close()
    
    def clearDb(self):
        open(self.dbName, 'w').close()
        
    
    def store(self, data):
        # self.file = open(self.dbName, 'a+')
        self.file.write(str(data) + "\n")
        self._size += 1
    
    def find(self, key, value):
        self.openDb()
        for document in self.file:
            document = eval(document)
            if(document[key] == value):
                return document
        return None
    
    def size(self):
        return self._size
    
    def show(self):
        self.openDb()
        return self.file.read()