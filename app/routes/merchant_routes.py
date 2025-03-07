from flask import Blueprint, jsonify
from flask_restx import Resource, fields
from app.services.merchant_service import MerchantService
from app.utils.response import success, error
from app import api

bp = Blueprint('merchant', __name__, url_prefix='/merchants')
ns = api.namespace('merchants', description='商家管理接口')

# 基础响应模型
response_model = api.model('Response', {
    'code': fields.Integer(description="响应码：1成功，-1失败"),
    'msg': fields.String(description="响应信息"),
    'data': fields.Raw(description="响应数据")
})

# 定义模型
merchant_model = api.model('Merchant', {
    'id': fields.Integer(readonly=True, description='商家ID'),
    'name': fields.String(required=True, description='商家名称'),
    'contact_person': fields.String(required=True, description='联系人'),
    'phone': fields.String(required=True, description='电话'),
    'address': fields.String(required=True, description='地址'),
    'created_at': fields.DateTime(readonly=True, description='创建时间'),
    'updated_at': fields.DateTime(readonly=True, description='更新时间')
})

# 分页请求模型
page_request = api.model('PageRequest', {
    'page': fields.Integer(required=False, default=1, description='页码，从1开始'),
    'per_page': fields.Integer(required=False, default=10, description='每页数量')
})

# 分页响应模型
page_response = api.model('PageResponse', {
    'items': fields.List(fields.Nested(merchant_model)),
    'total': fields.Integer(description='总记录数')
})

merchant_list_response = api.model('MerchantList', {
    'merchants': fields.List(fields.Nested(merchant_model))
})

merchant_id_request = api.model('MerchantId', {
    'id': fields.Integer(required=True, description='商家ID')
})

@ns.route('/list')
class MerchantList(Resource):
    @ns.doc('获取所有商家')
    @ns.expect(page_request)
    @ns.response(200, 'Success', response_model)
    def post(self):
        """获取商家列表（分页）"""
        try:
            data = api.payload or {}
            page = data.get('page', 1)
            per_page = data.get('per_page', 10)
            result = MerchantService.get_all_merchants(page, per_page)
            return success(data=result)
        except Exception as e:
            return error(str(e))

@ns.route('/detail')
class MerchantDetail(Resource):
    @ns.doc('获取商家详情')
    @ns.expect(merchant_id_request)
    @ns.response(200, 'Success', response_model)
    def post(self):
        """获取特定商家的详细信息"""
        try:
            data = api.payload
            merchant_id = data.get('id')
            if not merchant_id:
                return error("缺少商家ID")
            merchant = MerchantService.get_merchant_by_id(merchant_id)
            return success(data=merchant.to_dict())
        except Exception as e:
            return error(str(e))

@ns.route('/create')
class MerchantCreate(Resource):
    @ns.doc('创建新商家')
    @ns.expect(merchant_model)
    @ns.response(200, 'Success', response_model)
    def post(self):
        """创建新的商家"""
        try:
            merchant = MerchantService.create_merchant(api.payload)
            return success(data=merchant.to_dict())
        except Exception as e:
            return error(str(e))

@ns.route('/update')
class MerchantUpdate(Resource):
    @ns.doc('更新商家信息')
    @ns.expect(merchant_model)
    @ns.response(200, 'Success', response_model)
    def post(self):
        """更新商家信息"""
        try:
            data = api.payload
            merchant_id = data.get('id')
            if not merchant_id:
                return error("缺少商家ID")
            merchant = MerchantService.update_merchant(merchant_id, data)
            return success(data=merchant.to_dict())
        except Exception as e:
            return error(str(e))

@ns.route('/delete')
class MerchantDelete(Resource):
    @ns.doc('删除商家')
    @ns.expect(merchant_id_request)
    @ns.response(200, 'Success', response_model)
    def post(self):
        """删除指定商家"""
        try:
            data = api.payload
            merchant_id = data.get('id')
            if not merchant_id:
                return error("缺少商家ID")
            MerchantService.delete_merchant(merchant_id)
            return success(msg="删除成功")
        except Exception as e:
            return error(str(e)) 