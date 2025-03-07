from app.models.batch import Batch
from app.models.collar import Collar
from app import db

class BatchService:
    @staticmethod
    def create_batch(merchant_id, collar_count):
        """
        创建新批次并生成项圈
        """
        # 创建批次
        batch = Batch(merchant_id=merchant_id, collar_count=collar_count)
        db.session.add(batch)
        db.session.flush()  # 获取批次ID
        
        # 生成项圈
        collars = []
        for _ in range(collar_count):
            collar = Collar(
                merchant_id=merchant_id,
                batch_id=batch.id,
                collar_code=Collar.generate_code()
            )
            collars.append(collar)
        
        db.session.bulk_save_objects(collars)
        db.session.commit()
        return batch
    
    @staticmethod
    def get_all_batches(page=1, per_page=10):
        """
        获取所有批次
        """
        pagination = Batch.query.order_by(Batch.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total
        }
    
    @staticmethod
    def get_merchant_batches(merchant_id, page=1, per_page=10):
        """
        获取指定商家的批次
        """
        pagination = Batch.query.filter_by(merchant_id=merchant_id)\
            .order_by(Batch.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total
        }
    
    @staticmethod
    def get_batch_collars(batch_id, page=1, per_page=10):
        """
        获取指定批次的项圈
        """
        pagination = Collar.query.filter_by(batch_id=batch_id)\
            .order_by(Collar.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total
        } 