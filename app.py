from supabase import create_client, Client
from flask import Flask, request, redirect, render_template, url_for, session, jsonify
import sqlite3
from datetime import datetime, timedelta

from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from flask import Flask, request, redirect, render_template, url_for, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxqaXNta2JubXd2dWlzdmlieWthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMzk5MDUsImV4cCI6MjA1NDYxNTkwNX0.S48FLYIvSSba25TBcWlWfoLFbMIZywHaRDi0pI3SBRM'
csrf = CSRFProtect(app)




url: str = "https://ljismkbnmwvuisvibyka.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxqaXNta2JubXd2dWlzdmlieWthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMzk5MDUsImV4cCI6MjA1NDYxNTkwNX0.S48FLYIvSSba25TBcWlWfoLFbMIZywHaRDi0pI3SBRM"


supabase: Client = create_client(url, key)




app = Flask(__name__)

csrf = CSRFProtect(app)

app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from Supabase
        response = supabase.table('users_detail').select('*').eq('email', email).execute()
        user = response.data

        if user and check_password_hash(user[0]['password'], password):
            # Password is correct, store user details in session
            session['user_detail'] = user[0]
            return redirect(url_for('dashboard'))
        elif user:
            return 'Incorrect password'
        else:
            return redirect(url_for('signup'))  # Redirect to signup if the email doesn't exist
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']

        # Fetch user from Supabase
        response = supabase.table('users_detail').select('*').eq('email', email).execute()
        user = response.data

        if user:
            # Hash the new password and update the user record
            hashed_password = generate_password_hash(new_password)
            supabase.table('users_detail').update({'password': hashed_password}).eq('email', email).execute()
            return 'Password updated successfully'
        else:
            return 'Email not found'
    return render_template('forgot_password.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match"

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Check if email already exists
        response = supabase.table('users_detail').select('*').eq('email', email).execute()
        if len(response.data) > 0:
            return "Email already exists!"

        # Insert user details into the database
        supabase.table('users_detail').insert({

            'email': email,
            'password': hashed_password
        }).execute()

        # Store user information in the session (to manage login state)
        session['user_email'] = email
        session['username'] = username

        # Redirect to dashboard
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Fetch the latest IOP reading from the database
    response_latest = supabase.table('iopreading_data').select('*').order('measurement_time', desc=True).limit(1).execute()

    # Fetch all IOP readings to calculate average, highest, and lowest readings
    response_all = supabase.table('iopreading_data').select('*').execute()

    # Debugging: Print out the responses to check if data is being fetched correctly
    print("Latest Reading Response:", response_latest.data)
    print("All Readings Response:", response_all.data)

    # Default values if no data is found
    latest_iop = 22  # Default reading if none exists
    last_updated = "Just now"
    avg_reading = 0
    max_reading = 0
    min_reading = 0

    # Check if data exists for the latest reading
    if response_latest.data:
        latest_iop = response_latest.data[0]['pressure_value']
        last_updated = response_latest.data[0]['measurement_time']

    # Check if data exists for all readings
    if response_all.data:
        readings = [entry['pressure_value'] for entry in response_all.data]
        avg_reading = sum(readings) / len(readings) if readings else 0
        max_reading = max(readings) if readings else 0
        min_reading = min(readings) if readings else 0

    # Debugging: Print the calculated values
    print(f"Latest IOP: {latest_iop}, Average: {avg_reading}, Max: {max_reading}, Min: {min_reading}")

    return render_template(
        'dashboard.html', 
        latest_iop=latest_iop, 
        last_updated=last_updated,
        avg_reading=avg_reading,
        max_reading=max_reading,
        min_reading=min_reading
    )



@app.route('/take_new_reading', methods=['POST'])
def take_new_reading():
    # Fetch the latest IOP reading from the database
    response = supabase.table('iopreading_data').select('*').order('measurement_time', desc=True).limit(1).execute()

    # Check if data exists
    if response.data:
        latest_iop = response.data[0]['pressure_value']
        last_updated = response.data[0]['measurement_time']
    else:
        latest_iop = 22  # Dummy data if no reading exists
        last_updated = "Just now"

    # Pass the latest reading and update time to the dashboard
    return render_template('dashboard.html', latest_iop=latest_iop, last_updated=last_updated)






@app.route('/get-records', methods=['GET'])
def get_records():
    date = request.args.get('date')
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT date, time, iop, status FROM records WHERE date = ?", (date,))
    rows = cursor.fetchall()
    connection.close()
    records = [{'date': row[0], 'time': row[1], 'iop': row[2], 'status': row[3]} for row in rows]
    return jsonify(records)



@app.route('/previous-records', methods=['GET'])

@app.route('/records', methods=['GET'])
def records():
    # Get date filter from the request (if any)
    date_filter = request.args.get('start_date')
    if date_filter:
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d')  # Convert to datetime

    # Fetch records from Supabase
    records_data = supabase.table('iopreading_data').select('pressure_value', 'measurement_time').gt('pressure_value', 22).execute()

    # Convert Supabase response to list of dictionaries with status
    records = []
    for record in records_data.data:
        status = 'high' if record['pressure_value'] > 22 else 'normal'
        records.append({'pressure_value': record['pressure_value'], 'measurement_time': record['measurement_time'], 'status': status})

    # Apply the date filter (if provided)
    if date_filter:
        filtered_records = [r for r in records if datetime.strptime(r['measurement_time'], '%Y-%m-%d') >= date_filter]
    else:
        filtered_records = records

    # Pagination logic
    page = request.args.get('page', 1, type=int)  # Default page is 1 if not provided
    per_page = 5  # Records per page
    total_records = len(filtered_records)

    # Calculate the start and end index for the current page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_records = filtered_records[start:end]

    # Pagination info to pass to the frontend
    total_pages = (total_records + per_page - 1) // per_page  # Calculate the total number of pages
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    return render_template('previous-records.html', 
                           records=paginated_records, 
                           avg_pressure=sum(r['pressure_value'] for r in paginated_records) / len(paginated_records) if paginated_records else 0,
                           max_pressure=max(r['pressure_value'] for r in paginated_records) if paginated_records else 0,
                           min_pressure=min(r['pressure_value'] for r in paginated_records) if paginated_records else 0,
                           current_page=page, 
                           total_records=total_records, 
                           per_page=per_page, 
                           total_pages=total_pages, 
                           next_page=next_page, 
                           prev_page=prev_page,
                           date_filter=date_filter)

@app.route("/doctor-sugesstions")
def doctor():
    return render_template('doctor-suggestion.html')

if __name__ == "__main__":
    app.run(debug=True)