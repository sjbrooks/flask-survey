from flask import Flask, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fluffy'

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def handle_first_request():
    """Renders a page that shows the user the title
    of the survey, the instructions, and a button to
    start the survey. The button should serve as a link
    that directs the user to /questions/0"""

    return render_template('base.html', question_number=0)

@app.route('/questions/<question_number>')
def handle_button_click(question_number):
    """Handles the click of the start button and redirects
    to the next question of the survey"""

    if question_number in locals():
        question_number = int(question_number)
    else:
        question_number = 0
    next_question = question_number + 1
    question_text = satisfaction_survey.questions[question_number].question
    question_choices = satisfaction_survey.questions[question_number].choices

    return render_template('question_template.html', 
                            next_question=next_question, 
                            question_number=next_question, 
                            question_choices=question_choices)