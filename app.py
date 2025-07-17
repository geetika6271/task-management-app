import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database setup (SQLite)
DATABASE = 'tasks.db'

def get_db():
    """Open a new database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allow access to rows as dictionaries
    return conn

def init_db():
    """Initialize the database with the required table"""
    with app.app_context():
        db = get_db()
        db.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
        ''')
        db.commit()

@app.route('/')
def index():
    """Display all tasks"""
    db = get_db()
    cur = db.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task"""
    task_name = request.form.get('task')
    if task_name:
        db = get_db()
        db.execute('INSERT INTO tasks (name, done) VALUES (?, ?)', (task_name, False))
        db.commit()
    return redirect(url_for('index'))

@app.route('/mark_done/<int:task_id>')
def mark_done(task_id):
    """Mark a task as done"""
    db = get_db()
    db.execute('UPDATE tasks SET done = ? WHERE id = ?', (True, task_id))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task"""
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
