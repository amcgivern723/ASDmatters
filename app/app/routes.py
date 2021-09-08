from flask import render_template, flash, request, redirect, url_for
from app import app, db
from app.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user
from app.models import User ,Achievement
import json

#possible achievements user can ger
possible_achievements = [
    "Taken the test for the first time",
    "Beat your previous quiz score",
    "Achieved 100% in the quiz for the first time",
    "Achieved 100% in the quiz three times in a row"
]

#route for the about page
@app.route('/about')
def about():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('about.html', title='About page')

#route for the learning zone
@app.route('/learningZone')
def learningZone():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('learningZone.html', title='LearningZone')

#when the user selects the emotion they want to watch the resources for it will redirect them there chosen page
@app.route('/angry')
def angry():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('angry.html', title='Angry')

@app.route('/anxious')
def anxious():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('anxious.html', title='Anxious')

@app.route('/bored')
def bored():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('bored.html', title='Bored')

@app.route('/confused')
def confused():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('confused.html', title='Confused')

@app.route('/contempt')
def contempt():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('contempt.html', title='Contempt')

@app.route('/disappointed')
def disappointed():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('disappointed.html', title='Disappointed')

@app.route('/disgust')
def disgust():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('disgust.html', title='Disgust')

@app.route('/fear')
def fear():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('fear.html', title='Fear')

@app.route('/happy')
def happy():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('happy.html', title='Happy')

@app.route('/sad')
def sad():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('sad.html', title='Sad')

@app.route('/scared')
def scared():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('scared.html', title='Scared')

@app.route('/surprised')
def surprised():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('surprised.html', title='Surprised')


@app.route('/')
@app.route('/index')
@app.route('/quiz')
def quiz():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    with open('app/questions.json', 'r') as jfile:
        questions = json.load(jfile)
    return render_template('quiz.html', username=current_user.username, questions=questions, title='Quiz page')

def add_achievement(new_progress):
    # If this is the first progress for user
    if not current_user.progress:
        new_ach = [0]
        if int(new_progress) == 100:
            new_ach.append(2)
        return new_ach
    # If user has achieved highest possible achievement
    hundred = False
    for ach in current_user.achievements:
        if ach.number == 3:
            return []
        elif ach.number == 2:
            hundred = True
    # If the user just got a 100%, and doesn't have that achievement already
    new_ach = []
    progresses = current_user.progress[:-1].split(',')
    if not hundred:
        if int(new_progress) == 100:
            new_ach.append(2)
        # if this is your new high score
        previous_max = 0
        for p in progresses:
            if p and int(p) > previous_max:
                previous_max = int(p)
        if int(new_progress) > int(previous_max):
            new_ach.append(1)
    # If this is the 3rd 100 in a row
    if int(new_progress) == 100 and len(progresses) >= 2:
        if int(progresses[-1]) == 100 and int(progresses[-2]) == 100:
            new_ach.append(3)
    return new_ach

#progress route
@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        for new_ach_num in add_achievement(request.json['value']):
            new_ach = Achievement(
                number=new_ach_num, 
                name=possible_achievements[new_ach_num],
                user_id=current_user.id
            )
            db.session.add(new_ach)
        current_user.add_progress(request.json['value'])
        db.session.commit()
        return ('', 204)
    scores = None
    if current_user.progress:
        scores = json.dumps(current_user.progress[:-1].split(','))
    return render_template('progress.html', username=current_user.username,
        scores=scores)

#acheievements route
@app.route ('/achievements', methods=['GET'])
def achievements():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('achievements.html', username=current_user.username,
        achievements=current_user.achievements)

#login route 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('quiz'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Invalid username or password {}'.format(form.username.data))
            flash('Invalid username or password')
            return redirect(url_for('quiz'))
        login_user(user)
        return redirect(url_for('quiz'))
    return render_template('login.html', title='Sign In', form=form)

#signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('quiz'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print('Username already taken! {}'.format(form.username.data))
            flash('Username already taken!')
            return redirect(url_for('signup'))
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print('Congratulations, you are now a registered user!')
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('quiz'))
    return render_template('login.html', title='Sign up', form=form)

#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))











