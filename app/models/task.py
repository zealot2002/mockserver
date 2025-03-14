from datetime import datetime
from enum import Enum
from app import db

class RecurrenceType(str, Enum):
    NONE = 'none'  # 一次性任务
    DAILY = 'daily'  # 每日任务
    WEEKLY = 'weekly'  # 每周任务
    MONTHLY = 'monthly'  # 每月任务

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Cage(db.Model):
    __tablename__ = 'cage'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    warehouse = db.relationship('Warehouse', backref='cages')

class TaskTemplate(db.Model):
    __tablename__ = 'task_template'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    recurrence_type = db.Column(db.Enum(RecurrenceType), nullable=False, default=RecurrenceType.NONE)
    estimated_duration = db.Column(db.Integer)  # 预计任务时长（分钟）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('task_template.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    status = db.Column(db.String(20), default='PENDING')
    scheduled_time = db.Column(db.DateTime, nullable=False)
    completed_time = db.Column(db.DateTime)
    actual_duration = db.Column(db.Integer)  # 实际任务时长（分钟）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    template = db.relationship('TaskTemplate', backref='tasks')
    warehouse = db.relationship('Warehouse', backref='tasks')
    assignee = db.relationship('Employee', backref='tasks')
    cages = db.relationship('Cage', secondary='task_cage', backref='tasks')

    @property
    def name(self):
        return self.template.name

    @property
    def description(self):
        return self.template.description

    @property
    def is_recurring(self):
        return self.template.recurrence_type != RecurrenceType.NONE

class TaskCage(db.Model):
    __tablename__ = 'task_cage'
    
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    cage_id = db.Column(db.Integer, db.ForeignKey('cage.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Employee(db.Model):
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
