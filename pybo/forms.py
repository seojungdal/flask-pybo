# 검증

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField # 짧은 글, 긴글, 패스워드, 이메일
from wtforms.validators import DataRequired, length, EqualTo, Email # 값 필수여부
# validators 검증
# 필드 추가

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField(' 내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired('사용자 이름을 입력하세요'), length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력하세요'), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호를 입력하세요')])
    email = EmailField('이메일', [DataRequired('이메일을 입력하세요'), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired('사용자 이름을 입력하세요'), length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])

