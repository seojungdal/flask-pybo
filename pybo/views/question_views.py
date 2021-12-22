from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db
from pybo.models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required # 데코레이터 함수 호술
bp = Blueprint('question', __name__, url_prefix='/question') # Blueprint 클래스로 bp 객체 생성

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1) # ?page=1 / URL에서 page값 가져옴 없으면 맨 처음엔 없으니 기본값인 1
    question_list = Question.query.order_by(Question.create_date.desc()) # 내림차순 정렬 / 리스트임
    question_list = question_list.paginate(page, per_page=10) # 페이지당 10개씩해서 페이지 나눈 객체 생성
    return render_template('question/question_list.html', question_list=question_list)
    # html 안에 있는 question_list 변수에 question_list 대입
    # 렌더 템플릿은 해당 html을 화면에 표시

@bp.route('/detail/<int:question_id>/') # 메인페이지에서 클릭하면 해당 question의 id가 question_id로 삽입됨
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id) # question_id 가 맞는 Question 객체 넘겨줌
    return render_template('question/question_detail.html', question=question, form=form) # 오류확인에 form 사용

@bp.route('/create/', methods=('GET', 'POST')) # 저장버튼 눌렀을 때 POST 방식으로 전송
@login_required # 해당 함수 실행
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit(): # 폼을 생성할 때 각 필드에 지정한 DataRequired() 점검항목 이상여부
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # GET 방식이면 페이지 등록 페이지 다시 표시 / 맨처음 이 화면 표시 됨 → html에서 POST 시 데이터 저장됨
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question.id))

    if request.method == 'POST': # 저장하기 눌렀을 경우(POST 방식으로 요청)
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)  # form 변수에 들어있는 데이터(화면입력 데이터)를 question 객체에 적용
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question.id))
    else: # (1) 아이디 맞으면 여기부터 시작(처음은 GET 방식)
         form = QuestionForm(obj=question) # 데이터 베이스에서 조회한 데이터를 obj 매개변수에 전달하여 폼을 생성

    return render_template('question/question_form.html', form=form) # 질문수정을 눌렀을 경우(맨처음)(GET방식으로 요청)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id)) # 기존_id 그대로 보냄
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

