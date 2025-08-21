const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const cors = require('cors');

const DATABASE = 'todos.db';

const db = new sqlite3.Database(DATABASE, (err) => {
    if (err) {
        console.error('Error opening database', err.message);
    } else {
        console.log('Connected to the SQLite database.');
        db.run(`CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )`, (err) => {
            if (err) {
                console.error('Error creating table', err.message);
            } else {
                console.log('Table "todos" is ready.');
            }
        });
    }
});

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));


app.route('/api/tasks')
    .get((req, res) => {
        db.all('SELECT id, title, completed, created_at FROM todos ORDER BY created_at DESC', [], (err, rows) => {
            if (err) {
                res.status(500).json({ 'error': err.message });
                return;
            }
            res.json(rows);
        });
    })
    .post((req, res) => {
        const { title } = req.body;
        if (!title) {
            return res.status(400).json({ 'error': 'Title is required' });
        }
        const createdAt = new Date().toISOString();
        const sql = 'INSERT INTO todos (title, created_at) VALUES (?, ?)';
        
        // The `function()` syntax is used here to get access to `this.lastID`.
        db.run(sql, [title, createdAt], function(err) {
            if (err) {
                res.status(500).json({ 'error': err.message });
                return;
            }
            // Return the newly created task object.
            res.status(201).json({
                id: this.lastID,
                title: title,
                completed: 0,
                created_at: createdAt
            });
        });
    });

app.route('/api/tasks/:id')
    .patch((req, res) => {
        const { completed } = req.body;
        if (completed === undefined) {
            return res.status(400).json({ 'error': 'Missing "completed" field' });
        }
        const completedInt = completed ? 1 : 0;
        const sql = 'UPDATE todos SET completed = ? WHERE id = ?';
        
        db.run(sql, [completedInt, req.params.id], function(err) {
            if (err) {
                res.status(500).json({ 'error': err.message });
                return;
            }
            if (this.changes === 0) {
                 return res.status(404).json({ message: 'Task not found' });
            }
            res.json({ 'message': 'Task updated successfully' });
        });
    })
    .delete((req, res) => {
        const sql = 'DELETE FROM todos WHERE id = ?';
        db.run(sql, req.params.id, function(err) {
            if (err) {
                res.status(500).json({ 'error': err.message });
                return;
            }
            if (this.changes === 0) {
                return res.status(404).json({ message: 'Task not found' });
            }
            res.json({ 'message': 'Task deleted successfully' });
        });
    });

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
