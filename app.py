from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'truefit_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///truefit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load ML model
model = joblib.load('model/career_model.pkl')
encoder = joblib.load('model/label_encoder.pkl')

# ─── DATABASE MODELS ───────────────────────────────────────
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assessments = db.relationship('Assessment', backref='user', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    technical_skills = db.Column(db.String(500))
    soft_skills = db.Column(db.String(500))
    education = db.Column(db.String(200))
    experience = db.Column(db.String(200))
    career_interest = db.Column(db.String(200))
    top_career = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ─── HELPER FUNCTION ───────────────────────────────────────
def predict_careers(technical, soft, education, experience, interest, top_n=5):
    combined = f"{technical} {soft} {education} {experience} {interest}"
    proba = model.predict_proba([combined])[0]
    top_indices = np.argsort(proba)[::-1][:top_n]
    results = []
    for idx in top_indices:
        career = encoder.classes_[idx]
        confidence = round(proba[idx] * 100, 1)
        results.append({'career': career, 'confidence': confidence})
    return results

# ─── ROUTES ────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
@login_required
def form():
    return render_template('form.html')

@app.route('/results', methods=['POST'])
@login_required
def results():
    technical = request.form.get('technical_skills', '')
    soft = request.form.get('soft_skills', '')
    education = request.form.get('education', '')
    experience = request.form.get('experience', '')
    interest = request.form.get('career_interest', '')
    num = int(request.form.get('num_recommendations', 5))

    predictions = predict_careers(technical, soft, education, experience, interest, num)

    assessment = Assessment(
        user_id=current_user.id,
        technical_skills=technical,
        soft_skills=soft,
        education=education,
        experience=experience,
        career_interest=interest,
        top_career=predictions[0]['career'] if predictions else 'Unknown'
    )
    db.session.add(assessment)
    db.session.commit()

    return render_template('results.html',
        predictions=predictions,
        top_career=predictions[0]['career'] if predictions else 'Unknown',
        top_confidence=predictions[0]['confidence'] if predictions else 0,
        user_name=current_user.name,
        technical=technical,
        soft=soft
    )

@app.route('/dashboard')
@login_required
def dashboard():
    assessments = Assessment.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html',
        assessments=assessments,
        total=len(assessments)
    )

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/market')
def market():
    return render_template('market.html')

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

# ─── AUTH ROUTES ───────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists!')

        hashed = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('form'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('form'))
        return render_template('login.html', error='Invalid email or password!')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ─── PDF EXPORT ────────────────────────────────────────────
@app.route('/export-pdf', methods=['POST'])
@login_required
def export_pdf():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from flask import make_response
    import io

    top_career = request.form.get('top_career', 'Unknown')
    predictions_raw = request.form.get('predictions', '')

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFillColor(colors.HexColor('#2563eb'))
    c.rect(0, height-100, width, 100, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height-50, "TrueFit AI - Career Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height-75, f"Generated for: {current_user.name}")

    c.setFillColor(colors.HexColor('#1e293b'))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height-140, f"Best Career Match: {top_career}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height-170, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    c.drawString(50, height-195, f"Powered by: Random Forest ML Model")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height-235, "Your Top Career Recommendations:")

    y = height - 265
    for i, line in enumerate(predictions_raw.split(',')):
        if line.strip():
            c.setFont("Helvetica", 12)
            c.drawString(70, y, f"{i+1}. {line.strip()}")
            y -= 25

    c.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=TrueFit_Career_Report.pdf'
    return response

# ─── INIT DB ───────────────────────────────────────────────
with app.app_context():
    db.create_all()
    print("✅ Database ready!")

if __name__ == '__main__':
    app.run(debug=True, port=5000)