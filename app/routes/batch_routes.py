from flask import Blueprint
from flask_restx import Resource, fields
from app.services.batch_service import BatchService
from app.utils.response import success, error
from app import api

bp = Blueprint('batch', __name__, url_prefix='/batches')
ns = api.namespace('batches', description='批次管理接口')

# 模型定义
batch_model = api.model('Batch', {
    'id': fields.Integer(readonly=True, description='批次ID'),
    'merchant_id': fields.Integer(required=True, description='商家ID'),
    'merchant_name': fields.String(readonly=True, description='商家名称'),
    'collar_count': fields.Integer(required=True, description='项圈数量'),
    'created_at': fields.DateTime(readonly=True, description='创建时间')
})

collar_model = api.model('Collar', {
    'id': fields.Integer(readonly=True, description='项圈ID'),
    'merchant_id': fields.Integer(readonly=True, description='商家ID'),
    'merchant_name': fields.String(readonly=True, description='商家名称'),
    'batch_id': fields.Integer(readonly=True, description='批次ID'),
    'collar_code': fields.String(readonly=True, description='项圈编码'),
    'created_at': fields.DateTime(readonly=True, description='创建时间')
})

# 创建批次请求模型
create_batch_request = api.model('CreateBatchRequest', {
    'merchant_id': fields.Integer(required=True, description='商家ID'),
    'collar_count': fields.Integer(required=True, description='项圈数量')
})

# 分页请求模型
page_request = api.model('PageRequest', {
    'page': fields.Integer(required=False, default=1, description='页码'),
    'per_page': fields.Integer(required=False, default=10, description='每页数量')
})

# 商家批次请求模型
merchant_batch_request = api.model('MerchantBatchRequest', {
    'merchant_id': fields.Integer(required=True, description='商家ID'),
    'page': fields.Integer(required=False, default=1, description='页码'),
    'per_page': fields.Integer(required=False, default=10, description='每页数量')
})

# 批次项圈请求模型
batch_collar_request = api.model('BatchCollarRequest', {
    'batch_id': fields.Integer(required=True, description='批次ID')
})

@ns.route('/create')
class BatchCreate(Resource):
    @ns.doc('创建新批次')
    @ns.expect(create_batch_request)
    def post(self):
        """创建新批次并生成项圈"""
        try:
            data = api.payload
            batch = BatchService.create_batch(
                data['merchant_id'],
                data['collar_count']
            )
            return success(data=batch.to_dict())
        except Exception as e:
            return error(str(e))

@ns.route('/list')
class BatchList(Resource):
    @ns.doc('获取所有批次')
    @ns.expect(page_request)
    def post(self):
        """获取所有批次列表"""
        try:
            data = api.payload or {}
            result = BatchService.get_all_batches(
                page=data.get('page', 1),
                per_page=data.get('per_page', 10)
            )
            return success(data=result)
        except Exception as e:
            return error(str(e))

@ns.route('/merchant/list')
class MerchantBatchList(Resource):
    @ns.doc('获取商家批次')
    @ns.expect(merchant_batch_request)
    def post(self):
        """获取指定商家的批次列表"""
        try:
            data = api.payload
            result = BatchService.get_merchant_batches(
                merchant_id=data['merchant_id'],
                page=data.get('page', 1),
                per_page=data.get('per_page', 10)
            )
            return success(data=result)
        except Exception as e:
            return error(str(e))

@ns.route('/collars')
class BatchCollarList(Resource):
    @ns.doc('获取批次项圈')
    @ns.expect(batch_collar_request)
    def post(self):
        """获取指定批次的所有项圈"""
        try:
            data = api.payload
            result = BatchService.get_batch_collars(
                batch_id=data['batch_id']
            )
            return success(data=result)
        except Exception as e:
            return error(str(e)) 