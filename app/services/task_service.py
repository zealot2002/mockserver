from datetime import datetime, timedelta
from app import db
from app.models.task import Task, TaskTemplate, Warehouse, Cage, Employee, TaskCage, RecurrenceType, TaskStatus

class TaskService:
    @staticmethod
    def create_task_template(data):
        """创建任务模板"""
        template = TaskTemplate(
            name=data['name'],
            description=data.get('description', ''),
            recurrence_type=data.get('recurrence_type', RecurrenceType.NONE),
            estimated_duration=data.get('estimated_duration')
        )
        
        db.session.add(template)
        db.session.commit()
        return template

    @staticmethod
    def get_task_templates(is_recurring=None):
        """获取任务模板列表"""
        query = TaskTemplate.query
        
        if is_recurring is not None:
            if is_recurring:
                query = query.filter(TaskTemplate.recurrence_type != RecurrenceType.NONE)
            else:
                query = query.filter(TaskTemplate.recurrence_type == RecurrenceType.NONE)
            
        return query.all()

    @staticmethod
    def get_task_template(template_id):
        """获取任务模板详情"""
        return TaskTemplate.query.get(template_id)

    @staticmethod
    def update_task_template(template_id, data):
        """更新任务模板"""
        template = TaskTemplate.query.get(template_id)
        if not template:
            raise ValueError('Template not found')

        template.name = data.get('name', template.name)
        template.description = data.get('description', template.description)
        template.recurrence_type = data.get('recurrence_type', template.recurrence_type)

        template.estimated_duration = data.get('estimated_duration', template.estimated_duration)

        db.session.commit()
        return template

    @staticmethod
    def delete_task_template(template_id):
        """删除任务模板"""
        template = TaskTemplate.query.get(template_id)
        if not template:
            raise ValueError('Template not found')

        db.session.delete(template)
        db.session.commit()

    @staticmethod
    def create_task(data):
        """基于模板创建任务"""
        template = TaskTemplate.query.get(data['template_id'])
        if not template:
            raise ValueError('Template not found')

        task = Task(
            template_id=template.id,
            warehouse_id=data['warehouse_id'],
            assignee_id=data['assignee_id'],
            scheduled_time=datetime.strptime(data['scheduled_time'], '%Y-%m-%d %H:%M:%S'),
            status=TaskStatus.PENDING
        )
        
        db.session.add(task)
        db.session.flush()
        
        # 添加笼舍关联
        if 'cage_id' in data:
            task_cage = TaskCage(task_id=task.id, cage_id=data['cage_id'])
            db.session.add(task_cage)
        
        db.session.commit()
        return task

    @staticmethod
    def create_tasks_for_cages(data):
        """为多个猫笼创建任务"""
        template = TaskTemplate.query.get(data['template_id'])
        if not template:
            raise ValueError('Template not found')

        tasks = []
        scheduled_time = datetime.strptime(data['scheduled_time'], '%Y-%m-%d %H:%M:%S')

        # 为每个笼舍创建任务
        for cage_id in data['cage_ids']:
            task_data = {
                'template_id': template.id,
                'warehouse_id': data['warehouse_id'],
                'assignee_id': data['assignee_id'],
                'scheduled_time': scheduled_time.strftime('%Y-%m-%d %H:%M:%S'),
                'cage_id': cage_id
            }
            tasks.append(TaskService.create_task(task_data))

        return tasks

    @staticmethod
    def get_task_list(filters=None):
        """获取任务列表"""
        query = Task.query
        
        if filters:
            if 'status' in filters:
                query = query.filter(Task.status == filters['status'])
            if 'assignee_id' in filters:
                query = query.filter(Task.assignee_id == filters['assignee_id'])
            if 'warehouse_id' in filters:
                query = query.filter(Task.warehouse_id == filters['warehouse_id'])
            if 'template_id' in filters:
                query = query.filter(Task.template_id == filters['template_id'])

            if 'start_date' in filters:
                query = query.filter(Task.scheduled_time >= filters['start_date'])
            if 'end_date' in filters:
                query = query.filter(Task.scheduled_time <= filters['end_date'])
        
        return query.all()

    @staticmethod
    def start_task(task_id):
        """开始任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError('Task not found')

        if task.status != TaskStatus.PENDING:
            raise ValueError('Task can only be started when in PENDING status')

        task.status = TaskStatus.IN_PROGRESS
        db.session.commit()
        return task

    @staticmethod
    def complete_task(task_id, actual_duration):
        """完成任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError('Task not found')

        if task.status != TaskStatus.IN_PROGRESS:
            raise ValueError('Task can only be completed when in IN_PROGRESS status')

        task.status = TaskStatus.COMPLETED
        task.completed_time = datetime.utcnow()
        task.actual_duration = actual_duration
        
        db.session.commit()
        return task

    @staticmethod
    def get_worker_tasks(worker_id, status=None):
        """获取工人的任务列表"""
        query = Task.query.filter(Task.assignee_id == worker_id)
        
        if status:
            query = query.filter(Task.status == status)
            
        return query.order_by(Task.scheduled_time).all()



    @staticmethod
    def get_task_detail(task_id):
        """获取任务详情"""
        return Task.query.get(task_id)

    @staticmethod
    def delete_task(task_id):
        """删除任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError('Task not found')
            
        db.session.delete(task)
        db.session.commit()
