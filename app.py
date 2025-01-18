from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit')
def employer_page():
    return render_template("submit.html")

@app.route("/postings")
def job_listings():
    return render_template('postings.html')

@app.route("/admin_login")
def admin_portal():
    return render_template("admin_login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")