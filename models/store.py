from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    # keep the mapping dynamic orelse if you have lot of data
    # it will take up a lot of resources

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find(cls, name):
        return cls.query.filter_by(name=name).first() # 'SELECT * FROM items WHERE name=? LIMIT 1'
    # it returns the class object directly. Yaay!!

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit() 