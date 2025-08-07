import sqlite3
import datetime
from flask import Flask, request, jsonify, g

DATABASE = 'todos.db'
app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row

    db.execute("""
               CREATE TABLE IF NOT EXISTS todos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     completed INTEGER NOT NULL DEFAULT 0,
                     created_at TEXT NOT NULL
                   )
               """)
    db.commit()
    return db

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    db = get_db()
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400

        title = data['title']
        created_at = datetime.datetime.now().isoformat()

        cursor = db.execute(
            'INSERT INTO todos (title, created_at) VALUES (?, ?)',
            (title, created_at)
        )
        db.commit()
        
        return jsonify({
            'id': cursor.lastrowid,
            'title': title,
            'completed': 0,
            'created_at': created_at
        }), 201

    else:
        cursor = db.execute('SELECT id, title, completed, created_at FROM todos ORDER BY created_at DESC')
        tasks = [dict(row) for row in cursor.fetchall()]
        return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['PATCH', 'DELETE'])
def handle_task(task_id):
    db = get_db()
    if request.method == 'PATCH':
        data = request.get_json()
        if 'completed' not in data:
            return jsonify({'error': 'Missing "completed" field'}), 400
        
        # Convert boolean to integer (1 for true, 0 for false)
        completed = 1 if data['completed'] else 0
        
        db.execute(
            'UPDATE todos SET completed = ? WHERE id = ?',
            (completed, task_id)
        )
        db.commit()
        return jsonify({'message': 'Task updated successfully'})

    elif request.method == 'DELETE':
        db.execute('DELETE FROM todos WHERE id = ?', (task_id,))
        db.commit()
        return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=3000)