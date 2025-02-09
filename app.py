
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')
@app.route("/previous-records")
def records():
    return render_template('previous-records.html')

@app.route("/doctor-suggestions")
def doctor():
    return render_template('doctor-suggestion.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
