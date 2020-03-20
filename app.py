from flask import Flask, request, render_template, flash, redirect
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
    that directs the user to /questions/0."""

    return render_template('survey_home_template.html', question_number=0)


@app.route('/answer', methods=["POST"])
def collect_data():
    selected_option = request.form['answer']
    # print('this is our requested form info ', selected_option)

    responses.append(selected_option)
    print("!!!!!!!!THESE ARE RESPONSES \n \n ",responses)

    print(' \n \n The number of responses was', f'{len(responses)}', ' \n \n')
    print(' \n \n The number of questions is this survey is', f'{len(satisfaction_survey.questions)}', '\n \n')

    if len(responses)==len(satisfaction_survey.questions):
        print('\n \n YOU ARE DONE \n \n')
        redirect('/thanks')
    else:
        print('\n \n This redirects to question ID', f'{len(responses)}', ' \n \n')
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:question_number>')
def handle_button_click(question_number):
    """Handles the click of the buttons and directs
    to the next question of the survey"""

    # print("Printing question nubmer before if else", question_number)

    next_question = question_number + 1
    question_text = satisfaction_survey.questions[question_number].question
    question_choices = satisfaction_survey.questions[question_number].choices

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