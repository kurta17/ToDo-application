from flask import Flask, flash, redirect, render_template, request, session, url_for
import json
import os
import uuid
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure instance folder exists
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

users_file = os.path.join(app.instance_path, 'users.json')

# Load users from file
def load_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

# Save users to file
def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f)

users = load_users()

class User(UserMixin):
    def __init__(self, email, user_dict):
        self.id = user_dict['id']
        self.email = email
        self.password = user_dict['password']
        self.name = user_dict['name']
        super().__init__()

class UserRegistration(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')

@login_manager.user_loader
def get_user(id):
    for email, user_dict in users.items():
        if user_dict['id'] == id:
            return User(email, user_dict)
    return None

def load_to_do_list(user_id):
    try:
        with open(os.path.join(app.instance_path, f'{user_id}_to_do.txt'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_to_do_list(user_id, to_do_list):
    with open(os.path.join(app.instance_path, f'{user_id}_to_do.txt'), 'w') as f:
        json.dump(to_do_list, f)

def check_login(email, password):
    if email in users:
        if password == users[email]['password']:
            return True
    return False

@app.route('/')
def home():
    greeting = current_user.name if current_user.is_authenticated else 'Guest'
    return render_template('home.html', greeting=greeting)

@app.route('/toggle-dark-mode')
def toggle_dark_mode():
    redirect_to = request.args.get('redirectto')
    session['dark_mode'] = not session.get('dark_mode', False)
    return redirect(redirect_to)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if check_login(email, password):
            user = get_user(users[email]['id'])
            login_user(user)
            flash('You are now logged in', 'success')
            return redirect(url_for('home'))
        flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistration()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        
        user_id = str(uuid.uuid4())
        users[email] = {'id': user_id, 'password': password, 'name': name}
        save_users(users)

        user = get_user(user_id)
        login_user(user)
        
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/to-do')
@login_required
def to_do_list():
    to_do = load_to_do_list(current_user.id)
    return render_template('to_do.html', to_do=to_do)

@app.route('/add-task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        to_do = load_to_do_list(current_user.id)
        to_do.append(task)
        save_to_do_list(current_user.id, to_do)
        return redirect(url_for('to_do_list'))
    return render_template('add_task.html')

@app.route('/delete-task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    to_do = load_to_do_list(current_user.id)
    task_id -= 1
    if 0 <= task_id < len(to_do):
        task_removed = to_do.pop(task_id)
        save_to_do_list(current_user.id, to_do)
        flash(f'Task "{task_removed}" removed successfully', 'success')
    return redirect(url_for('to_do_list'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=4900)
