# app 생성 및 반환 / 블루프린트 적용 / 필터 등록
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


from flaskext.markdown import Markdown # 마크다운

# SQLite 오류 해결(1) 알 필요 없음
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(e): # 페이지 오류 시
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__) # Pybo 앱 생성
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM 초기화
    db.init_app(app)

    # SQLite 오류 해결(2) 알 필요 없음
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        # 기존 코드
        migrate.init_app(app, db)
    from . import models # migrate객체가 models.py 파일을 참조하게 함
    
    # 블루 프린트 적용
    from .views import main_views, question_views, anwser_views, auth_views, comment_views
    app.register_blueprint(main_views.bp) # main_views 모듈의 bp를  app에 등록
    app.register_blueprint(question_views.bp)
    app.register_blueprint(anwser_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)

    # 필터 등록 ← 필터 생성
    from .fliter import format_datetime # 함수
    app.jinja_env.filters['datetime'] = format_datetime

    # 마크다운 등록
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # 오류페이지
    app.register_error_handler(404, page_not_found)

    return app
