from flask import Flask, flash, json, redirect, render_template, request, url_for
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

def load_from_file():
    default_to_do = ["Go to the Gym", 
            "Call Family", 
            "Do Homework", 
            "Cook Dinner", 
            "Read a Book", 
            "Watch a Movie",
            "Go to Sleep"
            ]
    try:
        with open(app.instance_path + '/to_do.txt', 'r') as f:
            default_to_do = json.load(f)
    except FileNotFoundError:
        return default_to_do
    return default_to_do

to_do = load_from_file()

def save_to_do_list():
    with open(app.instance_path + '/to_do.txt', 'w') as f:
        json.dump(to_do, f)
        

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/to-do')
def to_do_list():
    return render_template('to_do.html', to_do=to_do)

@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        to_do.append(task)
        save_to_do_list()
        return redirect(url_for('to_do_list'))
    return render_template('add_task.html')

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task_id = int(task_id) - 1
    if 0 <= task_id < len(to_do):
        task_removed = to_do.pop(task_id)
        save_to_do_list()
        flash(f'Task " {task_removed} " removed successfully', 'success')
        return redirect(url_for('to_do_list'))

    

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, port=4900)
    

