from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from app.utils.response import success, error
from flasgger import swag_from

task_bp = Blueprint('task', __name__)

@task_bp.route('/admin/task-templates', methods=['POST'])
@swag_from({
    'tags': ['管理端-任务模板管理'],
    'summary': '创建任务模板',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': '模板名称'},
                    'description': {'type': 'string', 'description': '模板描述'},
                    'recurrence_type': {'type': 'string', 'enum': ['none', 'daily', 'weekly', 'monthly'], 'description': '任务类型，none为一次性任务，daily为每日任务，weekly为每周任务，monthly为每月任务'},
                    'estimated_duration': {'type': 'integer', 'description': '预计任务时长（分钟）'}
                },
                'required': ['name', 'recurrence_type']
            }
        }
    ],
    'responses': {
        200: {
            'description': '创建成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'template_id': {'type': 'integer', 'description': '模板ID'}
                        }
                    }
                }
            }
        }
    }
})
def create_task_template():
    """创建任务模板"""
    try:
        data = request.get_json()
        template = TaskService.create_task_template(data)
        return success({'template_id': template.id}, 'Template created successfully')
    except Exception as e:
        return error(str(e))

@task_bp.route('/admin/task-templates', methods=['GET'])
@swag_from({
    'tags': ['管理端-任务模板管理'],
    'summary': '获取任务模板列表',
    'parameters': [
        {
            'name': 'is_recurring',
            'in': 'query',
            'type': 'boolean',
            'description': '是否为周期任务模板'
        }
    ],
    'responses': {
        200: {
            'description': '获取成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'templates': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'description': {'type': 'string'},
                                        'recurrence_type': {'type': 'string'},

                                        'estimated_duration': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_task_templates():
    """获取任务模板列表"""
    try:
        is_recurring = request.args.get('is_recurring', type=lambda v: v.lower() == 'true' if v else None)
        templates = TaskService.get_task_templates(is_recurring)
        return success({
            'templates': [{
                'id': template.id,
                'name': template.name,
                'description': template.description,
                'recurrence_type': template.recurrence_type.value,

                'estimated_duration': template.estimated_duration
            } for template in templates]
        })
    except Exception as e:
        return error(str(e))



@task_bp.route('/admin/tasks', methods=['POST'])
@swag_from({
    'tags': ['管理端-任务管理'],
    'summary': '创建任务（支持批量创建）',
    'description': '创建任务，每个笼舍会生成一个独立的任务。如果任务模板是周期性的，系统会自动生成周期任务。',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'template_id': {'type': 'integer', 'description': '任务模板ID'},
                    'warehouse_id': {'type': 'integer', 'description': '仓库ID'},
                    'assignee_id': {'type': 'integer', 'description': '负责人ID'},
                    'scheduled_time': {'type': 'string', 'description': '计划执行时间，格式：YYYY-MM-DD HH:mm:ss'},
                    'cage_ids': {'type': 'array', 'items': {'type': 'integer'}, 'description': '笼舍ID列表（必填，每个笼舍将创建一个独立的任务）'}
                },
                'required': ['template_id', 'warehouse_id', 'assignee_id', 'scheduled_time', 'cage_ids']
            }
        }
    ],
    'responses': {
        200: {
            'description': '创建成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'tasks': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'description': {'type': 'string'},
                                        'status': {'type': 'string'},
                                        'scheduled_time': {'type': 'string'},
                                        'template': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'name': {'type': 'string'},
                                                'recurrence_type': {'type': 'string'}
                                            }
                                        },
                                        'cage': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'code': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def create_task():
    """创建任务（支持批量创建）"""
    try:
        data = request.get_json()
        tasks = TaskService.create_tasks_for_cages(data)
        return success({
            'tasks': [{
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'status': task.status,
                'scheduled_time': task.scheduled_time.strftime('%Y-%m-%d %H:%M:%S'),
                'template': {
                    'id': task.template.id,
                    'name': task.template.name,
                    'recurrence_type': task.template.recurrence_type.value
                },
                'cage': {
                    'id': task.cages[0].id if task.cages else None,
                    'code': task.cages[0].code if task.cages else None
                }
            } for task in tasks]
        })
    except Exception as e:
        return error(str(e))

@task_bp.route('/admin/tasks', methods=['GET'])
@swag_from({
    'tags': ['管理端-任务管理'],
    'summary': '获取任务列表',
    'parameters': [
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'description': '任务状态：PENDING/IN_PROGRESS/COMPLETED'
        },
        {
            'name': 'assignee_id',
            'in': 'query',
            'type': 'integer',
            'description': '负责人ID'
        },
        {
            'name': 'warehouse_id',
            'in': 'query',
            'type': 'integer',
            'description': '仓库ID'
        },

        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'description': '开始日期，格式：YYYY-MM-DD'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'description': '结束日期，格式：YYYY-MM-DD'
        }
    ],
    'responses': {
        200: {
            'description': '获取成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'tasks': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'description': {'type': 'string'},
                                        'status': {'type': 'string'},
                                        'scheduled_time': {'type': 'string'},
                                        'assignee': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'name': {'type': 'string'}
                                            }
                                        },
                                        'warehouse': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'name': {'type': 'string'}
                                            }
                                        },

                                        'cages': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'id': {'type': 'integer'},
                                                    'code': {'type': 'string'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_task_list():
    """获取任务列表"""
    try:
        filters = {
            'status': request.args.get('status'),
            'assignee_id': request.args.get('assignee_id'),
            'warehouse_id': request.args.get('warehouse_id'),

            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date')
        }
        # 移除None值的过滤条件
        filters = {k: v for k, v in filters.items() if v is not None}
        
        tasks = TaskService.get_task_list(filters)
        return success({
            'tasks': [{
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'status': task.status,
                'scheduled_time': task.scheduled_time.strftime('%Y-%m-%d %H:%M:%S'),
                'assignee': {
                    'id': task.assignee.id,
                    'name': task.assignee.name
                },
                'warehouse': {
                    'id': task.warehouse.id,
                    'name': task.warehouse.name
                },
                'template': {
                    'id': task.template.id,
                    'name': task.template.name,
                    'recurrence_type': task.template.recurrence_type.value
                },
                'cages': [{
                    'id': cage.id,
                    'code': cage.code
                } for cage in task.cages]
            } for task in tasks]
        })
    except Exception as e:
        return error(str(e))

@task_bp.route('/worker/tasks', methods=['GET'])
@swag_from({
    'tags': ['工人端-任务管理'],
    'summary': '获取工人的任务列表',
    'parameters': [
        {
            'name': 'worker_id',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': '工人ID'
        },
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'description': '任务状态：PENDING/IN_PROGRESS/COMPLETED'
        }
    ],
    'responses': {
        200: {
            'description': '获取成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'tasks': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'description': {'type': 'string'},
                                        'status': {'type': 'string'},
                                        'scheduled_time': {'type': 'string'},
                                        'warehouse': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'name': {'type': 'string'}
                                            }
                                        },
                                        'template': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'name': {'type': 'string'},
                                                'recurrence_type': {'type': 'string'}
                                            }
                                        },
                                        'cages': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'id': {'type': 'integer'},
                                                    'code': {'type': 'string'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_worker_tasks():
    """获取工人的任务列表"""
    try:
        worker_id = request.args.get('worker_id')
        status = request.args.get('status')
        
        if not worker_id:
            return error('Worker ID is required')
            
        tasks = TaskService.get_worker_tasks(worker_id, status)
        return success({
            'tasks': [{
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'status': task.status,
                'scheduled_time': task.scheduled_time.strftime('%Y-%m-%d %H:%M:%S'),
                'warehouse': {
                    'id': task.warehouse.id,
                    'name': task.warehouse.name
                },
                'template': {
                    'id': task.template.id,
                    'name': task.template.name,
                    'recurrence_type': task.template.recurrence_type.value
                },
                'cages': [{
                    'id': cage.id,
                    'code': cage.code
                } for cage in task.cages]
            } for task in tasks]
        })
    except Exception as e:
        return error(str(e))

@task_bp.route('/worker/tasks/<int:task_id>/complete', methods=['PUT'])
@swag_from({
    'tags': ['工人端-任务管理'],
    'summary': '完成任务',
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '任务ID'
        }
    ],
    'responses': {
        200: {
            'description': '更新成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'task_id': {'type': 'integer'},
                            'status': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def complete_task():
    """完成任务"""
    try:
        task_id = request.view_args['task_id']
        task = TaskService.update_task_status(task_id, 'COMPLETED')
        return success({
            'task_id': task.id,
            'status': task.status
        })
    except Exception as e:
        return error(str(e))


