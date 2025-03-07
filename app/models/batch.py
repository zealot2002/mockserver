from app import db
from datetime import datetime

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)
    collar_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'collar_count': self.collar_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } 