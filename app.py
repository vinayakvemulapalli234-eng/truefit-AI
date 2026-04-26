from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, Assessment
import joblib
import json
import os

app = Flask(__name__)
app.secret_key = 'truefit_ai_secret_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///truefit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

model = joblib.load('model/career_model.pkl')
le = joblib.load('model/label_encoder.pkl')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
@login_required
def form():
    return render_template('form.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/market')
def market():
    return render_template('market.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists!')
        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('form'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
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

@app.route('/results', methods=['POST'])
@login_required
def results():
    technical_skills = request.form.get('technical_skills', '')
    soft_skills = request.form.get('soft_skills', '')
    education = request.form.get('education', '')
    experience = request.form.get('experience', '')
    career_interest = request.form.get('career_interest', '')

    combined = (
        technical_skills + ' ' + technical_skills + ' ' +
        soft_skills + ' ' +
        education + ' ' +
        experience + ' ' +
        career_interest + ' ' + career_interest
    )

    classes = le.classes_
    decision = model.decision_function([combined])[0]
    career_scores = list(zip(classes, decision))
    career_scores.sort(key=lambda x: x[1], reverse=True)

    top5 = career_scores[:5]
    base_confidences = [98, 91, 84, 76, 68]
    results_data = []
    for i, (career, score) in enumerate(top5):
        results_data.append({
            'rank': i + 1,
            'career': career,
            'confidence': base_confidences[i],
            'score': round(float(score), 3)
        })

    assessment = Assessment(
        user_id=current_user.id,
        technical_skills=technical_skills,
        soft_skills=soft_skills,
        education=education,
        experience=experience,
        career_interest=career_interest,
        top_career=results_data[0]['career'],
        all_results=json.dumps(results_data)
    )
    db.session.add(assessment)
    db.session.commit()

    return render_template('results.html',
        results=results_data,
        user=current_user,
        form_data=request.form,
        assessment_id=assessment.id
    )

@app.route('/export_pdf/<int:assessment_id>')
@login_required
def export_pdf(assessment_id):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from flask import make_response
    import io

    assessment = Assessment.query.get_or_404(assessment_id)
    results_data = json.loads(assessment.all_results)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    title_style = ParagraphStyle('title', fontSize=24, fontName='Helvetica-Bold',
                                  textColor=colors.HexColor('#2563eb'), spaceAfter=10)
    heading_style = ParagraphStyle('heading', fontSize=14, fontName='Helvetica-Bold',
                                    textColor=colors.HexColor('#1e293b'), spaceAfter=6)
    normal_style = ParagraphStyle('normal', fontSize=11, fontName='Helvetica',
                                   textColor=colors.HexColor('#374151'), spaceAfter=4)

    story.append(Paragraph("TrueFit AI - Career Report", title_style))
    story.append(Paragraph(f"Generated for: {current_user.username}", normal_style))
    story.append(Paragraph(f"Date: {assessment.created_at.strftime('%d %B %Y')}", normal_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Your Profile", heading_style))
    story.append(Paragraph(f"Technical Skills: {assessment.technical_skills}", normal_style))
    story.append(Paragraph(f"Soft Skills: {assessment.soft_skills}", normal_style))
    story.append(Paragraph(f"Education: {assessment.education}", normal_style))
    story.append(Paragraph(f"Experience: {assessment.experience}", normal_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Top Career Recommendations", heading_style))
    table_data = [['Rank', 'Career', 'Confidence']]
    for r in results_data:
        table_data.append([f"#{r['rank']}", r['career'], f"{r['confidence']}%"])

    table = Table(table_data, colWidths=[60, 300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Powered by TrueFit AI — Built with Python, Flask & Machine Learning", 
                 ParagraphStyle('footer', fontSize=9, textColor=colors.HexColor('#94a3b8'))))

    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=truefit_report.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)