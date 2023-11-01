from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #members = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship('Project')

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


