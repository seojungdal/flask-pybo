from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/') # Blueprint 클래스로 bp 객체 생성

@bp.route('/') # 메인페이지
def index():
    return redirect(url_for('question._list')) # question 모듈 접두어 '/question' + _list함수의 라우트 '/list/' 반환
    # 리다이렉트 하게 되면 http://127.0.0.1:5000/*** 찾아감
