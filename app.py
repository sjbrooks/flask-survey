from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fluffy'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def handle_first_request():
    """Renders a page that shows the user the title
    of the survey, the instructions, and a button to
    start the survey. The button should serve as a link
    that directs the user to /questions/0."""

    responses = []

    return render_template('survey_home_template.html', question_number=0)


@app.route('/answer', methods=["POST"])
def collect_data():
    print('\n\n GOT INTO /ANSWER \n\n')
    selected_option = request.form['answer']

    responses.append(selected_option)
    print("!!!!!!!!THESE ARE RESPONSES \n \n ",responses)

    print(' \n \n The number of responses was', f'{len(responses)}', ' \n \n')
    print(' \n \n The number of questions is this survey is', f'{len(satisfaction_survey.questions)}', '\n \n')

    if len(responses)==len(satisfaction_survey.questions):
        print('\n \n YOU ARE DONE \n \n')
        return redirect('/thanks')
    else:
        print('\n \n This redirects to question ID', f'{len(responses)}', ' \n \n')
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:question_number>')
def handle_button_click(question_number):
    """Handles the click of the buttons and directs
    to the next question of the survey"""

    # print("Printing question nubmer before if else", question_number)

    next_question = len(responses) + 1
    question_text = satisfaction_survey.questions[question_number].question
    question_choices = satisfaction_survey.questions[question_number].choices

    if responses is None:
        return redirect('/')
    if len(responses)==len(satisfaction_survey.questions):
        print('\n \n YOU ARE DONE \n \n')
        return redirect('/thanks')
    if question_number != len(responses):
        flash(f'Invalid question id: {question_number}')
        return redirect(f"/questions/{len(responses)}")
    
    return render_template('question_template.html', 
                            next_question=next_question, 
                            question_number=next_question, 
                            question_choices=question_choices,
                            question_text=question_text)

@app.route('/thanks')
def end_of_survey():
    """Renders the thank you page at the end of the survey"""

    print("\n\n\nTHANK YOU FOR YOUR RESPONSE", responses, "\n\n\n")

    return render_template('thank_you.html')