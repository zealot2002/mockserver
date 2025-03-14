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

@task_bp.route('/admin/task-templates/list', methods=['POST'])
@swag_from({
    'tags': ['管理端-任务模板管理'],
    'summary': '获取任务模板列表',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'is_recurring': {'type': 'boolean', 'description': '是否为周期任务模板'}
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
        data = request.get_json()
        is_recurring = data.get('is_recurring')
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

@task_bp.route('/admin/tasks/list', methods=['POST'])
@swag_from({
    'tags': ['管理端-任务管理'],
    'summary': '获取任务列表',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': '任务状态：PENDING/IN_PROGRESS/COMPLETED'},
                    'assignee_id': {'type': 'integer', 'description': '负责人ID'},
                    'warehouse_id': {'type': 'integer', 'description': '仓库ID'},
                    'start_date': {'type': 'string', 'description': '开始日期，格式：YYYY-MM-DD'},
                    'end_date': {'type': 'string', 'description': '结束日期，格式：YYYY-MM-DD'}
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
        data = request.get_json()
        filters = {
            'status': data.get('status'),
            'assignee_id': data.get('assignee_id'),
            'warehouse_id': data.get('warehouse_id'),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date')
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

@task_bp.route('/worker/tasks/list', methods=['POST'])
@swag_from({
    'tags': ['工人端-任务管理'],
    'summary': '获取工人的任务列表',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'worker_id': {'type': 'integer', 'description': '工人ID'},
                    'status': {'type': 'string', 'description': '任务状态：PENDING/IN_PROGRESS/COMPLETED'}
                },
                'required': ['worker_id']
            }
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
        data = request.get_json()
        worker_id = data.get('worker_id')
        status = data.get('status')
        
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

@task_bp.route('/worker/tasks/start', methods=['POST'])
@swag_from({
    'tags': ['工人端-任务管理'],
    'summary': '开始任务',
    'description': '将任务状态从未开始更新为进行中',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'task_id': {'type': 'integer', 'description': '任务ID'}
                },
                'required': ['task_id']
            }
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
def start_task():
    """开始任务"""
    try:
        data = request.get_json()
        task_id = data.get('task_id')
        if not task_id:
            return error('Task ID is required')
        task = TaskService.start_task(task_id)
        return success({
            'task_id': task.id,
            'status': task.status.value
        })
    except Exception as e:
        return error(str(e))

@task_bp.route('/worker/tasks/complete', methods=['POST'])
@swag_from({
    'tags': ['工人端-任务管理'],
    'summary': '完成任务',
    'description': '将任务状态从进行中更新为已完成',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'task_id': {'type': 'integer', 'description': '任务ID'},
                    'actual_duration': {'type': 'integer', 'description': '实际耗时（分钟）'}
                },
                'required': ['task_id', 'actual_duration']
            }
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
                            'status': {'type': 'string'},
                            'completed_time': {'type': 'string'},
                            'actual_duration': {'type': 'integer'}
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
        data = request.get_json()
        task_id = data.get('task_id')
        actual_duration = data.get('actual_duration')
        if not task_id:
            return error('Task ID is required')
        if actual_duration is None:
            return error('Actual duration is required')
        task = TaskService.complete_task(task_id, actual_duration)
        return success({
            'task_id': task.id,
            'status': task.status.value,
            'completed_time': task.completed_time.strftime('%Y-%m-%d %H:%M:%S'),
            'actual_duration': task.actual_duration
        })
    except Exception as e:
        return error(str(e))
    except Exception as e:
        return error(str(e))


