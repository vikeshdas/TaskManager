import json

def test_create_task(client, auth_headers):
    data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    print("AUTHHEADER",auth_headers)
    response = client.post('/api/tasks', json=data, headers=auth_headers)
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
    client.post('/api/tasks', json=data, headers=auth_headers)

    response = client.get('/api/tasks/1', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['title'] == 'Test Task'

def test_update_task(client, auth_headers):

    data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    client.post('/api/tasks', json=data, headers=auth_headers)


    update_data = {
        'title': 'Updated Task',
        'completed': True
    }
    response = client.put('/api/tasks/1', json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Task updated successfully'

def test_delete_task(client, auth_headers):
    data = {
        'title': 'Test Task',
        'description': 'This is a test task'
    }
    client.post('/api/tasks', json=data, headers=auth_headers)

    response = client.delete('/api/tasks/1', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted successfully'