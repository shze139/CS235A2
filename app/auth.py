from flask import Blueprint,request,render_template,session,flash,redirect,url_for
from .forms import LoginForm,RegisterForm
from .repository import UsersRepository

bp = Blueprint('auth', __name__, url_prefix='/auth')
usersRepository = UsersRepository()

@bp.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = usersRepository.find_by_username(username)
        if user and user.get('password') == password:
            session['username'] = username
            return redirect(url_for('movie.index'))
        else:
            flash('Username or password is error', 'is-error')

    return render_template('login.html', form=form)

@bp.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = usersRepository.find_by_username(username)
        if user:
            flash('Username has been used.', 'is-error')
        else:
            flash('Register successful.', 'is-success')
            usersRepository.add_user(username, password)
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@bp.route('/logout', methods=('GET',))
def logout():
    session.pop('username', None)
    return redirect(url_for('movie.index'))

