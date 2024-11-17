from flask import Flask, request, redirect, render_template_string
import re
import pickle
import os

app = Flask(__name__)

# Global list to hold To Do items
todo_list = []

# Load list from file if it exists
file_name = 'todo_list.pkl'
if os.path.exists(file_name):
    with open(file_name, 'rb') as file:
        todo_list = pickle.load(file)

# HTML template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>To Do List</title>
</head>
<body>
    <h1>To Do List</h1>
    <table border="1">
        <tr>
            <th>Task</th>
            <th>Email</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
        {% for item in todo_list %}
        <tr>
            <td>{{ item['task'] }}</td>
            <td>{{ item['email'] }}</td>
            <td>{{ item['priority'] }}</td>
            <td>{{ 'Completed' if item['completed'] else 'Pending' }}</td>
            <td>
                {% if not item['completed'] %}
                <form action="/complete" method="post" style="display:inline;">
                    <input type="hidden" name="index" value="{{ loop.index0 }}">
                    <input type="submit" value="Mark as Completed">
                </form>
                {% endif %}
                <form action="/delete" method="post" style="display:inline;">
                    <input type="hidden" name="index" value="{{ loop.index0 }}">
                    <input type="submit" value="Delete">
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>

    <h2>Add New To Do Item</h2>
    <form action="/submit" method="post">
        Task: <input type="text" name="task" required><br>
        Email: <input type="email" name="email" required><br>
        Priority: 
        <select name="priority" required>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
        </select><br>
        <input type="submit" value="Add To Do Item">
    </form>

    <h2>Clear List</h2>
    <form action="/clear" method="post">
        <input type="submit" value="Clear">
    </form>

    <h2>Save List</h2>
    <form action="/save" method="post">
        <input type="submit" value="Save">
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, todo_list=todo_list)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    # Validate email
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return redirect('/')

    # Validate priority
    if priority not in ['Low', 'Medium', 'High']:
        return redirect('/')

    # Add item to the list
    todo_list.append({'task': task, 'email': email, 'priority': priority, 'completed': False})
    
    # Sort list by priority
    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    todo_list.sort(key=lambda x: priority_order[x['priority']])

    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    global todo_list
    todo_list = []
    return redirect('/')

@app.route('/save', methods=['POST'])
def save():
    with open(file_name, 'wb') as file:
        pickle.dump(todo_list, file)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    index = int(request.form.get('index'))
    if 0 <= index < len(todo_list):
        todo_list.pop(index)
    return redirect('/')

@app.route('/complete', methods=['POST'])
def complete():
    index = int(request.form.get('index'))
    if 0 <= index < len(todo_list):
        todo_list[index]['completed'] = True
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
