from flask import Blueprint,request,render_template,session,flash,redirect,url_for,abort
from .repository import MoviesRepository,ReviewsRepository, WatchListRepository
from .forms import SearchForm,ReviewForm
from datetime import datetime
from .decorators import login_required

bp = Blueprint('movie', __name__, url_prefix='/')
moviesRepository = MoviesRepository()
reviewsRepository = ReviewsRepository()
watchListRepository = WatchListRepository()

@bp.route('/', methods=('GET',))
def index():
    form = SearchForm(request.args, meta={'csrf': False})
    data = None
    if form.validate():
        page = form.page.data
        size = form.size.data
        key = form.key.data
        by = form.by.data
        data = moviesRepository.search(key, by, page, size)

    return render_template('index.html', data=data, form=form)

@bp.route('/movie/<id>', methods=('GET',))
def detail(id):
    movie = moviesRepository.find_by_id(id)
    reviews = reviewsRepository.find_by_movieId(id)
    reviewForm = ReviewForm(request.form)
    hasWatch = False
    if movie:
        status_code = 200
        if 'username' in session:
            hasWatch = watchListRepository.has_watch(session['username'], id)
    else:
        status_code = 404
    return render_template('movie.html', movie=movie, reviews=reviews, reviewForm=reviewForm, hasWatch=hasWatch), status_code

@bp.route('/add_review/<imdbID>', methods=('POST',))
@login_required
def add_review(imdbID):
    form = ReviewForm(request.form)
    if form.validate():
        createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = form.content.data
        username = session.get('username')
        reviewsRepository.add_review({
            'username': username,
            'content': content,
            'createtime': createtime,
            'imdbID': imdbID
        })
        flash('add review successful', 'is-success')
    else:
        flash('review content cannot be empty', 'is-error')
    return redirect(url_for('movie.detail', id=imdbID))

@bp.route('/add_to_watchlist/<imdbID>', methods=('GET',))
@login_required
def add_to_watchlist(imdbID):
    movie = moviesRepository.find_by_id(imdbID)
    if movie:
        username = session['username']
        watchListRepository.add({
            'username': username,
            'imdbID': imdbID
        })
        return redirect(url_for('movie.detail', id=imdbID))
    else:
        return abort(404)

@bp.route('/remove_from_watchlist/<imdbID>', methods=('GET',))
@login_required
def remove_from_watchlist(imdbID):
    movie = moviesRepository.find_by_id(imdbID)
    if movie:
        username = session['username']
        watchListRepository.remove({
            'username': username,
            'imdbID': imdbID
        })
        return redirect(url_for('movie.detail', id=imdbID))
    else:
        return abort(404)


@bp.route('/watchlist', methods=('GET',))
@login_required
def watchlist():
    username = session['username']
    watchlist = watchListRepository.find_by_username(username)
    for item in watchlist:
        item['movie'] = moviesRepository.find_by_id(item['imdbID'])
    return render_template('watchlist.html', watchlist=watchlist)


