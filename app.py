from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route("/")
def show_home():
    """Renders the home template"""
    return render_template('home.html', title=survey.title, instructions=survey.instructions)


@app.route("/start")
def start_survey():
    """Clears the session cookies of data to start fresh and redirects to the first question"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_questions(qid):
    """Checks for completion/question skipping, and renders the questions for the survey"""
    res = session.get(RESPONSES_KEY)
    if (res is None):
        return redirect('/')

    if (len(res) == len(survey.questions)):
        return redirect('/finish')

    if (len(res) != qid):
        flash(f"Invalid Question id: {qid}.")
        return redirect(f"/questions/{len(res)}")

    question = survey.questions[qid]
    return render_template('questions.html', qid=qid, question=question)


@app.route("/answer", methods=["POST"])
def handle_answers():
    """Checks for completion, adds data to the session cookies and redirects to next question"""
    answer = request.form["answer"]

    res = session[RESPONSES_KEY]
    res.append(answer)
    session[RESPONSES_KEY] = res
    if (len(res) == len(survey.questions)):
        return redirect('/finish')
    else:
        return redirect(f"/questions/{len(res)}")


@app.route("/finish")
def finish_survey():
    """Renders thank you page"""
    return render_template('thanks.html')
