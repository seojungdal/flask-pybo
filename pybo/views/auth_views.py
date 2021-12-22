from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools # 데코레이터 함수 생성에 필요

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth/')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # 첫번째로 매칭되는 객체만 달라
        if not user: # 없으면
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)
    # 처음엔 바로 return 실행

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): # 존재한다면 비밀번호 비교
            error = "비밀번호가 올바르지 않습니다."

        if error is None: # 에러가 없으면
            session.clear()
            session['user_id'] = user.id # session 에 저장
            return redirect(url_for('main.index'))

        flash(error) # 에러가 있으면 표시

    return render_template('auth/login.html', form=form)

@bp.before_app_request # 모든 라우트 함수보다 먼저 실행
def load_logged_in_user():
    user_id = session.get('user_id') # 세션에서 해당 키값 가져오기
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id) #

@bp.route('/logout/')
def logout():
    session.clear() # 세션 초기화
    return redirect(url_for('main.index'))

def login_required(view): # 다른 함수에서 @login_required 쓰면 해상함수 실행
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: # 없으면 리다이렉트
            return redirect(url_for('auth.login'))
        return view(**kwargs) # 있으면 원래 함수를 그대로 실행
    return wrapped_view
