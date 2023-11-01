from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Project
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        project = request.form.get('project')#Gets the project from the HTML 

        if len(project) < 1:
            flash('Project is too short!', category='error') 
        else:
            new_project = Project(data=project, user_id=current_user.id)  #providing the schema for the project 
            db.session.add(new_project) #adding the project to the database 
            db.session.commit()
            flash('Project added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-project', methods=['POST'])
def delete_project():  
    project = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    projectId = project['projectId']
    project = Project.query.get(projectId)
    if project:
        if project.user_id == current_user.id:
            db.session.delete(project)
            db.session.commit()

    return jsonify({})
