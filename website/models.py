from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

user_project = db.Table('user_project',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
                    )

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks = db.relationship('Task', backref='projects')
    #users = db.relationship('User')
    def __repr__(self):
        return f'<Project Id: "{self.id}" Data: {self.data}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    following = db.relationship('Project', secondary=user_project, backref='users')

    def __repr__(self):
        return f'<User Id: "{self.id} username: {self.user_name} Password: {self.password} First Name: {self.first_name}">'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))