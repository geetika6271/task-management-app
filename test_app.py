import os
import tempfile
import pytest
from app import app, init_db, get_db

@pytest.fixture
def client():
    # Create a temporary database file
    db_fd, temp_db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['DATABASE'] = temp_db_path

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(temp_db_path)

def test_index_page_loads(client):
    """Check if homepage loads with status 200 and correct title"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"My To-Do List" in response.data

def test_add_task(client):
    """Test adding a new task"""
    response = client.post('/add', data={'task': 'Write pytest tests'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Write pytest tests' in response.data

def test_mark_done(client):
    """Test marking a task as done"""
    client.post('/add', data={'task': 'Mark me done'}, follow_redirects=True)
    with app.app_context():
        db = get_db()
        task_id = db.execute("SELECT id FROM tasks WHERE name = ?", ('Mark me done',)).fetchone()['id']
    response = client.get(f'/mark_done/{task_id}', follow_redirects=True)
    assert b'class="task done"' in response.data

def test_delete_task(client):
    """Test deleting a task"""
    client.post('/add', data={'task': 'Delete me'}, follow_redirects=True)
    with app.app_context():
        db = get_db()
        task_id = db.execute("SELECT id FROM tasks WHERE name = ?", ('Delete me',)).fetchone()['id']
    response = client.get(f'/delete/{task_id}', follow_redirects=True)
    assert b'Delete me' not in response.data
