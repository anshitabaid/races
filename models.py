from config import  *
#model for Race database entry
class Race (db.Model):
    uid = db.Column (db.Integer, primary_key = True)
    p1=db.Column(db.Text())
    p2=db.Column(db.Text())
    w=db.Column(db.Text())
    def __init__(self, p1, p2, w):
        self.p1=p1
        self.p2=p2
        self.w = w

class Player (db.Model):
    uid = db.Column (db.Integer, primary_key = True)
    name = db.Column(db.Text())
    wins = db.Column(db.Integer, default=0)
    def __init__ (self, name):
        self.name = name
        self.wins = 0