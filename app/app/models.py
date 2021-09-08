from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    progress = db.Column(db.String(120), index=True, unique=True)
    achievements = db.relationship('Achievement', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_progress(self, new_score):
        if not self.progress:
           self.progress = ""
        self.progress += str(new_score) + ","

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    number = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<User {0} - Achievement: {1}>'.format(self.user.usernname, self.name)







