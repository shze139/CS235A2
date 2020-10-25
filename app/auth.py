from flask import Blueprint,request,render_template,session,flash,redirect,url_for
from .forms import LoginForm,RegisterForm
from .models.user import User
from .adapters.repository import repo_instance as repo

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = repo.get_user(username)
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('home.index'))
        else:
            flash('Username or password is error', 'is-error')

    return render_template('login.html', form=form)

@bp.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = repo.get_user(username)
        if user:
            flash('Username has been used.', 'is-error')
        else:
            flash('Register successful.', 'is-success')
            repo.add_user(User(username, password))
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@bp.route('/logout', methods=('GET',))
def logout():
    session.clear()
    return redirect(url_for('home.index'))

