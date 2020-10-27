from flask import Blueprint,request,render_template,session,flash,redirect,url_for,abort
from .forms import ReviewForm
from datetime import datetime
from .decorators import login_required
from .adapters.repository import repo_instance as repo
from .models.review import Review

bp = Blueprint('movie', __name__, url_prefix='/movie')

@bp.route('/<int:id>', methods=('GET',))
def detail(id):
    movie = repo.get_movie(id)
    reviews = repo.get_reviews_by_movie_id(id)
    reviewForm = ReviewForm(request.form)
    hasWatch = False
    if movie:
        status_code = 200
        if 'username' in session:
            hasWatch = repo.has_watch(session['username'], id)
    else:
        status_code = 404
    return render_template('movie.html', movie=movie, reviews=reviews, reviewForm=reviewForm, hasWatch=hasWatch), status_code

@bp.route('/add_review/<int:movieId>', methods=('POST',))
@login_required
def add_review(movieId):
    form = ReviewForm(request.form)
    if form.validate():
        timestamp = datetime.now()
        content = form.content.data
        username = session.get('username')
        repo.add_review(Review(content, timestamp, username, movieId))
        flash('add review successful', 'is-success')
    else:
        flash('review content cannot be empty', 'is-error')
    return redirect(url_for('movie.detail', id=movieId))

@bp.route('/add_to_watchlist/<int:movieId>', methods=('GET',))
@login_required
def add_to_watchlist(movieId):
    movie = repo.get_movie(movieId)
    if movie:
        username = session['username']
        repo.add_watch(username, movieId)
        return redirect(url_for('movie.detail', id=movieId))
    else:
        return abort(404)

@bp.route('/remove_from_watchlist/<int:movieId>', methods=('GET',))
@login_required
def remove_from_watchlist(movieId):
    movie = repo.get_movie(movieId)
    if movie:
        username = session['username']
        repo.remove_watch(username, movieId)
        return redirect(url_for('movie.detail', id=movieId))
    else:
        return abort(404)


@bp.route('/watchlist', methods=('GET',))
@login_required
def watchlist():
    username = session['username']
    movies = repo.get_watch_movies(username)
    return render_template('watchlist.html', movies=movies)


