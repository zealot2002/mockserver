from app.models.merchant import Merchant
from app import db

class MerchantService:
    @staticmethod
    def get_all_merchants(page=1, per_page=10):
        """
        获取商家列表，支持分页
        :param page: 页码，从1开始
        :param per_page: 每页数量
        :return: 商家列表和总数
        """
        pagination = Merchant.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total
        }
    
    @staticmethod
    def get_merchant_by_id(merchant_id):
        return Merchant.query.get_or_404(merchant_id)
    
    @staticmethod
    def create_merchant(data):
        merchant = Merchant(
            name=data['name'],
            contact_person=data['contact_person'],
            phone=data['phone'],
            address=data['address']
        )
        db.session.add(merchant)
        db.session.commit()
        return merchant
    
    @staticmethod
    def update_merchant(merchant_id, data):
        merchant = Merchant.query.get_or_404(merchant_id)
        merchant.name = data.get('name', merchant.name)
        merchant.contact_person = data.get('contact_person', merchant.contact_person)
        merchant.phone = data.get('phone', merchant.phone)
        merchant.address = data.get('address', merchant.address)
        db.session.commit()
        return merchant
    
    @staticmethod
    def delete_merchant(merchant_id):
        merchant = Merchant.query.get_or_404(merchant_id)
        db.session.delete(merchant)
        db.session.commit()
    
    @staticmethod
    def search_merchants(keyword):
        """
        根据关键字模糊查询商家
        :param keyword: 搜索关键字（商家名称、联系人、电话）
        :return: 商家列表
        """
        if not keyword:
            return []
            
        # 使用 or_ 组合多个条件
        merchants = Merchant.query.filter(
            db.or_(
                Merchant.name.like(f'%{keyword}%'),
                Merchant.contact_person.like(f'%{keyword}%'),
                Merchant.phone.like(f'%{keyword}%')
            )
        ).order_by(Merchant.created_at.desc()).all()
        
        return [merchant.to_dict() for merchant in merchants] 