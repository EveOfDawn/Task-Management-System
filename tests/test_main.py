import pytest
from flask import Flask
from website import create_app
from website.__init__ import db


def login(client, username, password):
    response = client.post(
        '/login',
        data={'user_name': username, 'password': password},
        follow_redirects=True
    )
    return response

def logout(client):
     response = client.get("/logout")
     return response

def signup(client, username, name, password1, password2):
     response = client.post(
            '/sign-up',
            data={'user_name': username,'firstName': name, 'password1': password1,
                   'password2' : password2},
            follow_redirects=True)
     return response

def test_landing (client):
    landing = client.get("/login")
    html = landing.data.decode()
    assert landing.status_code == 200
    assert '<h3 align="center">Login</h3>' in html
    assert landing.request.path == "/login"

#utest, ptest is correct, the others are not
@pytest.mark.parametrize(('username', 'password'),(
    #('', ''),
    ('utest', 'ptest'),
    #('utest', 'Wrong'),
    #('wrongu', 'ptest')
))
def test_login(client, username, password):
    response = login(client, username, password)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert b'Logged in successfully!' in response.data
    logout(client)

@pytest.mark.parametrize(('username', 'password'),(
    ('', ''),
    ('utest', 'Wrong'),
    ('wrongu', 'ptest')
))
def test_login_fails(client, username, password):
    response = login(client, username, password)
    assert response.status_code == 200
    assert response.request.path == "/login"
    #assert b'Logged in successfully!' in response.data
    logout(client)
''' 
#works, but needs a new username each time it is run
def test_signup(client):
    response = signup (client, 'u2test', 'test', 'ptest', 'ptest')
    assert response.status_code == 200
    assert response.request.path == "/"
'''
#black box input coverage partitioning technique
# ('') does not pass
@pytest.mark.parametrize(('name'), (
        ('t'), ('T'), (''), ('1'), ('='), (' ')
))
def test_create_project(client, name):
    login(client, 'utest','ptest')

    response = project_create(client, name)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert b'Project added!' in response.data


def project_create(client, name):
    response = client.post('/', data={'project' : name,},
                           follow_redirects=True)
    return response

@pytest.mark.parametrize(('i'), (
        (1), (2), (3)
))
def test_view_task(client, i):
    login(client, 'utest','ptest')
    name = 'test'
    project_create(client, name)
    response = client.get('/show-tasks?project_id=' + str(i),
                            follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/show-tasks'


def project_deletion(client, project_id):
    return client.post("/delete-project", data={'project' : project_id})


def test_project_deletion(client):
    login(client, 'utest','ptest')
    name = 'test'
    project_create(client, name)
    project_deletion(client, 1)
    
'''
def test_project_addMember(client):
    login(client, 'utest','ptest')
    name = 'test'
    project_create(client, name)
    response = client.post("/add-member", data= {'data' : 'Bob'})
    assert b"addMember success?" in response.data
    assert response.status_code == 200
    assert response.request.path == "/"
'''

    