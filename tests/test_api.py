import json
import random

task_id=""
def register_user(client, username, password):
    """
    Helper function to send a registration request to the /register endpoint.
    """
    data = {
        "username": username,
        "password": password,
    }
    response = client.post(
        "auth/register",
        data=json.dumps(data),
        content_type="application/json",
    )
    return response

def test_register_success(client):
    """
    Test successful user registration.
    """
    num=random.randint(1,100)
    response = register_user(
        client=client,
        username="testuser"+str(num),
        password="testpassword",
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "User registered successfully"


def test_register_missing_username_or_password(client):
    """
    Test registration with missing username or password.
    """

    response1 = register_user(
        client=client,
        username="",
        password="testpassword",
    )
    assert response1.status_code == 400
    data1 = json.loads(response1.data)
    assert data1["message"] == "Username and password required"
    num=random.randint(1,100)
    response2 = register_user(
        client=client,
        username="testuser"+str(num),
        password="",
    )
    assert response2.status_code == 400
    data2 = json.loads(response2.data)
    assert data2["message"] == "Username and password required"

def test_register_duplicate_username(client):
    """
    Test registration with a duplicate username.
    """
    response1 = register_user(
        client=client,
        username="testuser",
        password="testpassword",
    )
    # assert response1.status_code == 409

    response2 = register_user(
        client=client,
        username="testuser",
        password="testpassword",
    )

    assert response2.status_code == 409
    data = json.loads(response2.data)
    assert data["message"] == "User already exists"


def test_create_task(client, auth_headers):
    data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    print("AUTHHEADER",auth_headers)
    response = client.post('/api/tasks', json=data, headers=auth_headers)
    task_id = response.json['task']['id']
    print(task_id)
    print("status",response.status_code)
    assert response.status_code == 201


def test_get_tasks(client, auth_headers):
    response = client.get('/api/tasks', headers=auth_headers)
    assert response.status_code == 200
    assert 'tasks' in response.json
    assert isinstance(response.json['tasks'], list)

def test_get_task(client, auth_headers):
    data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    res = client.post('/api/tasks', json=data, headers=auth_headers)
    

    task_id = res.json['task']['id']  
    print("Task ID:", task_id)  
    

    response = client.get(f'/api/tasks/{task_id}', headers=auth_headers)  
    print("Response JSON:", response.json)  
   
    assert response.status_code == 200
    assert response.json['title'] == 'Test Task'



def test_update_task(client, auth_headers):

    data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    res = client.post('/api/tasks', json=data, headers=auth_headers)
    
    task_id = res.json['task']['id']
    print("Task ID:", task_id)  
    
    update_data = {
        'title': 'Updated Task',
        'completed': True
    }
    response = client.put(f'/api/tasks/{task_id}', json=update_data, headers=auth_headers)  
    print("Response JSON:", response.json)  
    
    assert response.status_code == 200
    assert response.json['message'] == 'Task updated successfully'


def test_delete_task(client, auth_headers):

    data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    res = client.post('/api/tasks', json=data, headers=auth_headers)
    

    task_id = res.json['task']['id']
    print("Task ID:", task_id) 
    
    response = client.delete(f'/api/tasks/{task_id}', headers=auth_headers)  
    print("Response JSON:", response.json) 
    
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted successfully'


def test_create_task_missing_title(client, auth_headers):
    """Test creating a task without a title."""
    data = {
        'description': 'This is a test task'
    }
    response = client.post('/api/tasks', json=data, headers=auth_headers)
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Title is required'


