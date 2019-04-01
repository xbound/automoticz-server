from automoticz.extensions import db


class TempLog(db.Model):
    ''' 
    Model for storing data about user.
    '''

    __tablename__ = 'templog'

    d = db.Column(db.String(30), nullable=False, unique=True)
    te = db.Column(db.String(30), nullable=True)
    hu = db.Column(db.String(30), nullable=True)

    def to_dict(self):
        return dict(d=self.d, te=self.te, hu=self.hu)

    def __repr__(self):
        return str(self.to_dict())