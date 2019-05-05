from automoticz.extensions import db


class UsageLog(db.Model):
    ''' 
    Model for storing data about user.
    '''

    __tablename__ = 'usagelog'

    log_id = db.Column(db.Integer, primary_key=True)
    idx = db.Column(db.Integer, nullable=False)
    user_idx = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    @staticmethod
    def from_dict(params: dict):
        idx = int(params['idx'])
        imp_idx = int(params['imp_idx'])
        date = params['date']
        status = params.get('data') or params.get('status')
        return UsageLog(
            idx=idx,
            imp_idx=imp_idx,
            date=date,
            status=status
        )

    def to_dict(self):
        return {
            'idx': self.idx,
            'user_idx': self.user_idx,
            'date': self.date,
            'status': self.status
        }