# OVERALL NOTES
# - adopt sentry or something similar for error reporting
# - database ought to have replicas and backups
# - adopt infra as code. ansible, terraform, cloudformation etc
# - adopt good git practices. work on feature branches, protect main branch, pr
#   workflow
# - create a test suite, run test suite in ci on commit
# - linting, autoformatting, ideally done in git hooks
import sqlite3
import datetime
from flask import Flask, request, jsonify, g

# move to actual database. maybe postgres
DATABASE = 'todos.db'
# move to a cdn. at some point
app = Flask(__name__, static_folder='public', static_url_path='')


# serve this direct from reverse proxy (nginx etc)
@app.route('/')
def index():
    return app.send_static_file('index.html')


def get_db():
    db = getattr(g, '_database', None)
    # as part of moving to an orm, evaluate needs as far as connection pooling,
    # maybe use pgbouncer as a service sidecar or some such
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row

    # adopt orm, either sqlalchemy or django would be good choices. if you
    # wanted the magic admin of django that would be a good decision criteria.

    # an orm will help by giving structured models that make retrieval easier
    # and also can enable automated database migrations thus making change over
    # time simpler to manage.
    # adopt database migrations, django migration or alembic in the case of sqlalchemy 

    # this needs a user column, user table
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

# add some basic documentation
# split the handlers to get and post
@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    db = get_db()
    if request.method == 'POST':
        data = request.get_json()
        # use pydantic or some other library to handle data validation instead
        # of manually handling it
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400

        title = data['title']
        # depending on the db maybe we want to just have this created at that
        # layer
        created_at = datetime.datetime.now().isoformat()

        # maybe wrap this in a transaction for future
        # if we wanted to scale this out:
        #  - shard data, could be based on geography, or hash of user id
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
        # call should support pagination, filtering
        tasks = [dict(row) for row in cursor.fetchall()]
        return jsonify(tasks)


# split out method handlers
@app.route('/api/tasks/<int:task_id>', methods=['PATCH', 'DELETE'])
def handle_task(task_id):
    db = get_db()
    if request.method == 'PATCH':
        data = request.get_json()
        # improve data validation as above
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
        # could add a deleted column to just mark as deleted instead of
        # actually deleting
        db.execute('DELETE FROM todos WHERE id = ?', (task_id,))
        db.commit()
        return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
