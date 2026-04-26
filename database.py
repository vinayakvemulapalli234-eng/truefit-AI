from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assessments = db.relationship('Assessment', backref='user', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    technical_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    education = db.Column(db.String(200))
    experience = db.Column(db.Text)
    career_interest = db.Column(db.String(200))
    top_career = db.Column(db.String(100))
    all_results = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)