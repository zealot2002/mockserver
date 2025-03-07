from app import db
from datetime import datetime
import uuid

class Collar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)
    collar_code = db.Column(db.String(32), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def generate_code():
        return uuid.uuid4().hex
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'batch_id': self.batch_id,
            'collar_code': self.collar_code,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } 