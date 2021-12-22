from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm() # AnswerForm 클래스의 객체 생성
    question = Question.query.get_or_404(question_id) # 해당 id의 Question클래스 객체 가져옴
    # question_detail.html의 {{ url_for('answer.create', question_id=question.id) }} 답변등록 눌렀을 때 question.id가 넘어옴
    if form.validate_on_submit():
        content = request.form['content'] # 'name' 속성이 content인 값 가져오기
        anwser = Answer(content=content, create_date=datetime.now(), user=g.user) # 값 넣기
        question.answer_set.append(anwser) # add 역할
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id)) # 기존 화면으로 돌아가기
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modify/<int:answer_id>', methods=('GET','POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question.id)) # 다시 질문으로 되돌아감
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id)) # 다시 질문으로 되돌아감
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form) # 맨 처음 페이지

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다.')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))