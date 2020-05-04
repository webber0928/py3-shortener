import datetime
from app import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(2040))
    alias = db.Column(db.String(10), unique=True)
    counts = db.Column(db.Integer, default=0)
    created = db.Column(db.Integer, default=datetime.datetime.now().timestamp())

    def __init__(self, *args, **kwargs):
        super(Url, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<URL %s>' % self.origin

class Count(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    counts = db.Column(db.Integer, default=1)
    date = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Count, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Count %d>' % self.date
