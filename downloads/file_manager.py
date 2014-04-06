from downloads import db
#from downloads import log
class FileManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(256))
    filename = db.Column(db.String(128))
    isdownloaded = db.Column(db.Integer,default=0)
    splits = db.Column(db.Integer,default=10)
    size = db.Column(db.Integer,default=0)
    block = db.Column(db.Integer,default=1490)
    sectors = db.relationship('sector', backref = 'fname', lazy = 'dynamic')
    
    def __init__(self):
        pass

    def infs(self,path,filename):
        data = self.query.filter_by(location = path, filename = filename ).first()
        return data

    def add(self,path,filename):
        self.location = path
        self.filename = filename
        db.session.add(self)
        db.session.commit()
        return self

    def query_update(self,path,filename,block):
        data = self.infs(path,filename)
        data.block = data.block + 1 
        db.session.add(data)
        db.session.commit()
        return data

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    def writefs(self,data,offset=0):
        with open(self.location + '/' + self.filename,'a') as f:
            f.seek(offset)
            f.write(data)
    
    def add_sectors(self):
        i = 0
        j = 0
        while i <= self.size:
            end = i + self.bock
            if  end > self.size:
                end = self.size
            Sectors.add(i,end,self)
            j = j + 1
        return j

    
    def __repr__(self):
        f = lambda x: x == 1 and 'donwloaded' or 'not downloaded' 
        return self.filename + ' total size: ' + str(self.size) + f(self.downloaded) 

            
class Sectors(db):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Integer,default=0)
    end = db.Column(db.Integer,default=0)
    isdownloaded = db.Column(db.Integer,default=0)
    size = db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('filemanager.id'))
    
    def __init__(self):
        pass

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def add(self,start,end,filestat):
        sec = Sectors(start = start, end = end , size = end - start, fname = filestat)
        db.session.add(sec)
        db.session.commit()
        return sec

    def __repr__(self):
        f = lambda x: x == 1 and ' donwloaded' or ' not downloaded' 
        return fname.location + "/" + fname.filename + ": " + "offset :" \
            + str(self.start) + '-' + self.end +  f(self.isdownloaded)
    
    
    