from flask import Flask, request, redirect, render_template,session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app, 'emailvalid')
app.secret_key="ThisisSecret!"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def submit():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
    else:
        flash("Success!")
        query="INSERT INTO email_address (email, created_at, updated_at) VALUES(:email,NOW(),NOW())"
        data={'email': request.form['email']}
        mysql.query_db(query,data)
        return redirect('/success')
    return redirect('/')

@app.route('/success')
def valide():
    query="SELECT email, DATE_FORMAT(created_at,'%b %D') FROM email_address"
    emails= mysql.query_db(query)
    return render_template('success.html', all_emails=emails)

app.run(debug=True)
