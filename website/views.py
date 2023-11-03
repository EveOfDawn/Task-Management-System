from __future__ import print_function # In python 2.7
import sys

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Project, User
from . import db
import json



views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        project = request.form.get('project')#Gets the project from the HTML 
        #member = request.form.get('member')
        #print(member, file=sys.stderr)
        if project:
            new_project = Project(data=project)#, user_id=current_user.id)  #providing the schema for the project 
            db.session.add(new_project) #adding the project to the database 
            db.session.commit()
            current_user.following.append(new_project)
            db.session.commit()
            flash('Project added!', category='success')
        
        
        else:
            #flash('Username does not exist', category='error')
            print('Username does not exist', file=sys.stderr)
        #return jsonify({})
        

    return render_template("home.html", user=current_user)


@views.route('/delete-project', methods=['POST'])
def delete_project(): 
    project = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    projectId = project['projectId']
    project = Project.query.get(projectId)
    
    if project:
        db.session.delete(project)
        db.session.commit()

    return jsonify({})

@views.route('/leave-project', methods=['POST'])
def leave_project():
    project = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    projectId = project['projectId']
    project = Project.query.get(projectId)
    
    if project:
        print(project.users, file=sys.stderr)
        for user in project.users: 
            if user == current_user:
                project.users.remove(user)
                db.session.commit()

    return jsonify({})

@views.route('/add-member', methods=['POST'])
def add_member():
    project = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    projectId = project['projectId']
    mem = project['mem']
    member = mem['member']
    project = Project.query.get(projectId)
    if member and project and (member != ''):
        user = User.query.filter_by(user_name=member).first()
        if user:
            user.following.append(project)
            db.session.commit()
    return jsonify({})

@views.route('/edit-member', methods=['POST'])
def edit_member():
    project = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    projectId = project['projectId']
    change = project['change']
    name_change = change['name_change']
    project = Project.query.get(projectId)
    print(project, file=sys.stderr)
    print(name_change, file=sys.stderr)
    if name_change and project and (name_change != ''):
        project.data = name_change
        db.session.add(project)
        db.session.commit()
    return jsonify({})