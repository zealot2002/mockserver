from flask import Blueprint, request
from app.services.batch_service import BatchService
from app.utils.response import success, error
from flasgger import swag_from

bp = Blueprint('batch', __name__, url_prefix='/batches')

@bp.route('/create', methods=['POST'])
@swag_from({
    'tags': ['批次管理'],
    'summary': '创建新批次',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'merchant_id': {'type': 'integer', 'description': '商家ID'},
                    'collar_count': {'type': 'integer', 'description': '项圈数量'}
                },
                'required': ['merchant_id', 'collar_count']
            }
        }
    ],
    'responses': {
        200: {
            'description': '创建成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 1},
                    'msg': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'merchant_id': {'type': 'integer'},
                            'merchant_name': {'type': 'string'},
                            'collar_count': {'type': 'integer'},
                            'created_at': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        }
    }
})
def create_batch():
        """创建新批次并生成项圈"""
        try:
            data = request.get_json()
            batch = BatchService.create_batch(
                data['merchant_id'],
                data['collar_count']
            )
            return success(data=batch.to_dict())
        except Exception as e:
            return error(str(e))

@bp.route('/list', methods=['POST'])
@swag_from({
    'tags': ['批次管理'],
    'summary': '获取所有批次',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'page': {'type': 'integer', 'description': '页码', 'default': 1},
                    'per_page': {'type': 'integer', 'description': '每页数量', 'default': 10}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': '获取成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 1},
                    'msg': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'items': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'merchant_id': {'type': 'integer'},
                                        'merchant_name': {'type': 'string'},
                                        'collar_count': {'type': 'integer'},
                                        'created_at': {'type': 'string', 'format': 'date-time'}
                                    }
                                }
                            },
                            'total': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def batch_list():
        """获取所有批次列表"""
        try:
            data = request.get_json() or {}
            result = BatchService.get_all_batches(
                page=data.get('page', 1),
                per_page=data.get('per_page', 10)
            )
            return success(data=result)
        except Exception as e:
            return error(str(e))

@bp.route('/merchant/list', methods=['POST'])
@swag_from({
    'tags': ['批次管理'],
    'summary': '获取商家批次',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'merchant_id': {'type': 'integer', 'description': '商家ID'},
                    'page': {'type': 'integer', 'description': '页码', 'default': 1},
                    'per_page': {'type': 'integer', 'description': '每页数量', 'default': 10}
                },
                'required': ['merchant_id']
            }
        }
    ],
    'responses': {
        200: {
            'description': '获取成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 1},
                    'msg': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'items': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'merchant_id': {'type': 'integer'},
                                        'merchant_name': {'type': 'string'},
                                        'collar_count': {'type': 'integer'},
                                        'created_at': {'type': 'string', 'format': 'date-time'}
                                    }
                                }
                            },
                            'total': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def merchant_batch_list():
        """获取指定商家的批次列表"""
        try:
            data = request.get_json()
            result = BatchService.get_merchant_batches(
                merchant_id=data['merchant_id'],
                page=data.get('page', 1),
                per_page=data.get('per_page', 10)
            )
            return success(data=result)
        except Exception as e:
            return error(str(e))

@bp.route('/collars', methods=['POST'])
@swag_from({
    'tags': ['批次管理'],
    'summary': '获取批次项圈',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'batch_id': {'type': 'integer', 'description': '批次ID'}
                },
                'required': ['batch_id']
            }
        }
    ],
    'responses': {
        200: {
            'description': '获取成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 1},
                    'msg': {'type': 'string'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'merchant_id': {'type': 'integer'},
                                'merchant_name': {'type': 'string'},
                                'batch_id': {'type': 'integer'},
                                'collar_code': {'type': 'string'},
                                'created_at': {'type': 'string', 'format': 'date-time'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def batch_collar_list():
        """获取指定批次的所有项圈"""
        try:
            data = request.get_json()
            result = BatchService.get_batch_collars(
                batch_id=data['batch_id']
            )
            return success(data=result)
        except Exception as e:
            return error(str(e)) 