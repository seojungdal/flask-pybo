import os

BASE_DIR = os.path.dirname(__file__)

# 파이보에 ORM 적용
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# 데이터베이스 접속주소 / pybo.db라는 '데이터베이스 파일'을 프로젝트의 루트 디렉터리(pybo폴더)에 저장
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"