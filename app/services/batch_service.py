from app.models.batch import Batch
from app.models.collar import Collar
from app.models.merchant import Merchant
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
        pagination = db.session.query(Batch, Merchant.name.label('merchant_name'))\
            .join(Merchant, Batch.merchant_id == Merchant.id)\
            .order_by(Batch.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        items = []
        for batch, merchant_name in pagination.items:
            item = batch.to_dict()
            item['merchant_name'] = merchant_name
            items.append(item)
            
        return {
            'items': items,
            'total': pagination.total
        }
    
    @staticmethod
    def get_merchant_batches(merchant_id, page=1, per_page=10):
        """
        获取指定商家的批次
        """
        pagination = db.session.query(Batch, Merchant.name.label('merchant_name'))\
            .join(Merchant, Batch.merchant_id == Merchant.id)\
            .filter(Batch.merchant_id == merchant_id)\
            .order_by(Batch.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        items = []
        for batch, merchant_name in pagination.items:
            item = batch.to_dict()
            item['merchant_name'] = merchant_name
            items.append(item)
            
        return {
            'items': items,
            'total': pagination.total
        }
    
    @staticmethod
    def get_batch_collars(batch_id):
        """
        获取指定批次的所有项圈
        """
        # 修改查询，使用 join 关联商家表和批次表
        collars = db.session.query(Collar, Merchant.name.label('merchant_name'))\
            .join(Merchant, Collar.merchant_id == Merchant.id)\
            .filter(Collar.batch_id == batch_id)\
            .order_by(Collar.created_at.desc())\
            .all()
        
        # 修改返回数据格式，添加商家名称
        items = []
        for collar, merchant_name in collars:
            item = collar.to_dict()
            item['merchant_name'] = merchant_name
            items.append(item)
            
        return {
            'items': items,
            'total': len(items)
        } 