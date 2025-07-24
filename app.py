from flask import (
    Flask, request, jsonify, render_template, redirect,
    url_for, flash, session, abort
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- Flask App & Database Setup ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.secret_key = 'dev'
db = SQLAlchemy(app)

# --- Models ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    important = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)

# --- REST API Endpoints ---
@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """Create a new task via API."""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid due date format'}), 400
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'Pending'),
        important=data.get('important', False),
        due_date=due_date
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id}), 201

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def api_update_task(id):
    """Update an existing task via API."""
    task = Task.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.important = data.get('important', task.important)
    due_date = data.get('due_date')
    if due_date:
        try:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid due date format'}), 400
    db.session.commit()
    return jsonify({'message': 'Task updated'})

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def api_delete_task(id):
    """Delete a task via API."""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """Get all tasks via API."""
    tasks = Task.query.with_entities(
        Task.id, Task.title, Task.description, Task.status,
        Task.created_at, Task.important, Task.due_date
    ).all()
    result = [
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'created_at': t.created_at.strftime('%Y-%m-%d %H:%M'),
            'important': t.important,
            'due_date': t.due_date.strftime('%Y-%m-%d') if t.due_date else None
        }
        for t in tasks
    ]
    return jsonify(result)

@app.route('/api/tasks/<int:id>', methods=['GET'])
def api_get_task(id):
    """Get a single task via API."""
    t = Task.query.get_or_404(id)
    return jsonify({
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'status': t.status,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M'),
        'important': t.important,
        'due_date': t.due_date.strftime('%Y-%m-%d') if t.due_date else None
    })

# --- Web UI Routes ---
@app.route('/', methods=['GET'])
def index():
    """Main page: show tasks with search, filter, sort, and pagination."""
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    sort = request.args.get('sort', 'created_at')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    query = Task.query
    if search:
        query = query.filter(
            Task.title.contains(search) | Task.description.contains(search)
        )
    if status:
        query = query.filter_by(status=status)
    query = query.order_by(Task.title) if sort == 'title' else query.order_by(Task.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items
    dark_mode = session.get('dark_mode', False)
    # Progress bar calculation
    total_tasks = query.count()
    completed_tasks = query.filter_by(status='Completed').count() if total_tasks > 0 else 0
    percent_complete = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    return render_template(
        'index.html',
        tasks=tasks,
        pagination=pagination,
        dark_mode=dark_mode,
        percent_complete=percent_complete,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks
    )

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task from the web UI."""
    title = request.form['title']
    description = request.form.get('description', '')
    due_date_str = request.form.get('due_date', '')
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid due date format!')
    new_task = Task(title=title, description=description, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    flash('Task created!')
    return redirect(url_for('index'))

@app.route('/toggle_dark_mode')
def toggle_dark_mode():
    """Toggle dark mode for the UI."""
    session['dark_mode'] = not session.get('dark_mode', False)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    """Edit an existing task from the web UI."""
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description', '')
        due_date_str = request.form.get('due_date', '')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid due date format!')
        else:
            task.due_date = None
        db.session.commit()
        flash('Task updated!')
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/task/<int:id>')
def task_detail(id):
    """Show details for a single task."""
    task = Task.query.get_or_404(id)
    return render_template('detail.html', task=task)

@app.route('/toggle_status/<int:id>')
def toggle_status(id):
    """Toggle a task's status between Pending and Completed."""
    task = Task.query.get_or_404(id)
    if task.status == 'Completed':
        task.status = 'Pending'
        flash('Task marked as pending!')
    else:
        task.status = 'Completed'
        flash('Task marked as completed!')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/important/<int:id>')
def important_task(id):
    """Toggle a task's important flag."""
    task = Task.query.get_or_404(id)
    task.important = not task.important
    db.session.commit()
    flash('Task marked as important!' if task.important else 'Task unmarked as important!')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_task(id):
    """Delete a task from the web UI (with confirmation)."""
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!')
        return redirect(url_for('index'))
    return render_template('delete_confirm.html', task=task)

# --- Main Entrypoint ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
