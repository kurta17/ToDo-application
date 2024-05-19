from flask import Flask, flash, json, redirect, render_template, request, session, url_for
import json
import os
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



users = {'kurta@gmail.com': {'password': '1234', 'name': 'Kurta'}}

class User(UserMixin):

    def __init__(self, email, user_dict):
        self.id = email
        self.password = user_dict['password']
        self.name = user_dict['name']

        super().__init__()

class UserRegistration(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    name = StringField('name')
    confirm_password = PasswordField('Confirm Password')



@login_manager.user_loader
def get_user(id: str) -> User:
    user_dict = users[id]
    return User(id, user_dict)


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


def save_to_do_list():
    with open(app.instance_path + '/to_do.txt', 'w') as f:
        json.dump(to_do, f)



to_do = load_from_file()

def check_login(email, password):
    if email in users:
        if password == users[email]['password']:
            return True
    return False
        

@app.route('/')
def home():
    if current_user.is_authenticated:
        greeting = current_user.name
    else:
        greeting = 'Guest'
    return render_template('home.html', greeting=greeting)

@app.route('/toggle-dark-mode')
def toggle_dark_mode():
    dir = request.args.get('redirectto')
    if 'dark_mode' in session:
        session.pop('dark_mode')
    else:
        session['dark_mode'] = True

    return redirect(dir)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if request.method == 'GET':
        logout_user()
        flash('You are now logged out', 'success')
        return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if check_login(email, password):
            user = get_user(email)
            login_user(user)
            return redirect(url_for('home'))
        flash('You are now logged in', 'success')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistration()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        
        users[email] = {'password': password, 'name': name}
        user = get_user(email)
        login_user(user)
        
        return redirect(url_for('home'))
    return render_template('register.html',form=form)

@app.route('/to-do')
@login_required
def to_do_list():
    
    return render_template('to_do.html', to_do=to_do)

@app.route('/add-task', methods=['GET', 'POST'])
@login_required
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
    print(users)
    app.run(debug=True, port=4900)
    

