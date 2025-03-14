from flask import Blueprint, request, jsonify
from app.services.merchant_service import MerchantService
from app.utils.response import success, error
from flasgger import swag_from

bp = Blueprint('merchant', __name__, url_prefix='/merchants')

@bp.route('/list', methods=['POST'])
@swag_from({
    'tags': ['商家管理'],
    'summary': '获取商家列表',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'page': {'type': 'integer', 'description': '页码，从1开始', 'default': 1},
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
                                        'name': {'type': 'string'},
                                        'contact_person': {'type': 'string'},
                                        'phone': {'type': 'string'},
                                        'address': {'type': 'string'},
                                        'created_at': {'type': 'string', 'format': 'date-time'},
                                        'updated_at': {'type': 'string', 'format': 'date-time'}
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
def merchant_list():
        """获取商家列表（分页）"""
        try:
            data = request.get_json() or {}
            page = data.get('page', 1)
            per_page = data.get('per_page', 10)
            result = MerchantService.get_all_merchants(page, per_page)
            return success(data=result)
        except Exception as e:
            return error(str(e))

@bp.route('/detail', methods=['POST'])
@swag_from({
    'tags': ['商家管理'],
    'summary': '获取商家详情',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': '商家ID'}
                },
                'required': ['id']
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
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'contact_person': {'type': 'string'},
                            'phone': {'type': 'string'},
                            'address': {'type': 'string'},
                            'created_at': {'type': 'string', 'format': 'date-time'},
                            'updated_at': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        }
    }
})
def merchant_detail():
        """获取特定商家的详细信息"""
        try:
            data = request.get_json()
            merchant_id = data.get('id')
            if not merchant_id:
                return error('缺少商家ID')
            merchant = MerchantService.get_merchant_by_id(merchant_id)
            return success(data=merchant.to_dict())
        except Exception as e:
            return error(str(e))

@bp.route('/create', methods=['POST'])
@swag_from({
    'tags': ['商家管理'],
    'summary': '创建新商家',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': '商家名称'},
                    'contact_person': {'type': 'string', 'description': '联系人'},
                    'phone': {'type': 'string', 'description': '电话'},
                    'address': {'type': 'string', 'description': '地址'}
                },
                'required': ['name', 'contact_person', 'phone', 'address']
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
                            'name': {'type': 'string'},
                            'contact_person': {'type': 'string'},
                            'phone': {'type': 'string'},
                            'address': {'type': 'string'},
                            'created_at': {'type': 'string', 'format': 'date-time'},
                            'updated_at': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        }
    }
})
def merchant_create():
        """创建新的商家"""
        try:
            data = request.get_json()
            merchant = MerchantService.create_merchant(data)
            return success(data=merchant.to_dict())
        except Exception as e:
            return error(str(e))

@bp.route('/update', methods=['POST'])
@swag_from({
    'tags': ['商家管理'],
    'summary': '更新商家信息',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': '商家ID'},
                    'name': {'type': 'string', 'description': '商家名称'},
                    'contact_person': {'type': 'string', 'description': '联系人'},
                    'phone': {'type': 'string', 'description': '电话'},
                    'address': {'type': 'string', 'description': '地址'}
                },
                'required': ['id']
            }
        }
    ],
    'responses': {
        200: {
            'description': '更新成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 1},
                    'msg': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'contact_person': {'type': 'string'},
                            'phone': {'type': 'string'},
                            'address': {'type': 'string'},
                            'created_at': {'type': 'string', 'format': 'date-time'},
                            'updated_at': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        }
    }
})
def merchant_update():
        """更新商家信息"""
        try:
            data = request.get_json()
            merchant_id = data.get('id')
            if not merchant_id:
                return error('缺少商家ID')
            merchant = MerchantService.update_merchant(merchant_id, data)
            return success(data=merchant.to_dict())
        except Exception as e:
            return error(str(e))

@bp.route('/delete', methods=['POST'])
@swag_from({
    'tags': ['商家管理'],
    'summary': '删除商家',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': '商家ID'}
                },
                'required': ['id']
            }
        }
    ],
    'responses': {
        200: {
            'description': '删除成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 1},
                    'msg': {'type': 'string'},
                    'data': {'type': 'object'}
                }
            }
        }
    }
})
def merchant_delete():
        """删除指定商家"""
        try:
            data = request.get_json()
            merchant_id = data.get('id')
            if not merchant_id:
                return error('缺少商家ID')
            MerchantService.delete_merchant(merchant_id)
            return success(msg='删除成功')
        except Exception as e:
            return error(str(e))

@bp.route('/search', methods=['POST'])
@swag_from({
    'tags': ['商家管理'],
    'summary': '搜索商家',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'keyword': {'type': 'string', 'description': '搜索关键字（商家名称、联系人、电话）'}
                },
                'required': ['keyword']
            }
        }
    ],
    'responses': {
        200: {
            'description': '搜索成功',
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
                                        'name': {'type': 'string'},
                                        'contact_person': {'type': 'string'},
                                        'phone': {'type': 'string'},
                                        'address': {'type': 'string'}
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
def merchant_search():
        """根据关键字搜索商家"""
        try:
            data = request.get_json()
            keyword = data.get('keyword', '').strip()
            if not keyword:
                return error('搜索关键字不能为空')
                
            merchants = MerchantService.search_merchants(keyword)
            return success(data={
                'items': merchants,
                'total': len(merchants)
            })
        except Exception as e:
            return error(str(e))

@bp.route('/get-by-collar', methods=['POST'])
@swag_from({
    'tags': ['商家管理'],
    'summary': '根据项圈获取商家',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'collar_code': {'type': 'string', 'description': '项圈序列号'}
                },
                'required': ['collar_code']
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
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'contact_person': {'type': 'string'},
                            'phone': {'type': 'string'},
                            'address': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def merchant_by_collar():
        """根据项圈序列号获取商家信息"""
        try:
            data = request.get_json()
            collar_code = data.get('collar_code', '').strip()
            if not collar_code:
                return error('项圈序列号不能为空')
                
            merchant = MerchantService.get_merchant_by_collar_code(collar_code)
            return success(data=merchant)
        except ValueError as e:
            return error(str(e))
        except Exception as e:
            return error(str(e)) 