
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def employer_submissions():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        company = request.form['company']
        email = request.form['email']
        new_job = Job(title=title, location=location, company=company, email=email)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('submit.html')

@app.route('/postings')
def job_postings():
    jobs = Job.query.filter_by(is_approved=True).all()
    return render_template('postings.html', jobs=jobs)

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        job_id = request.form['job_id']
        action = request.form['action']
        job = Job.query.get(job_id)
        if action == 'approve':
            job.is_approved = True
        elif action == 'delete':
            db.session.delete(job)
        db.session.commit()
    jobs = Job.query.all()
    return render_template('admin_panel.html', jobs=jobs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)