from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = "keep it a secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    mysql = connectToMySQL('email_validation')
    emails = mysql.query_db("SELECT * FROM emails")
    print(emails)
    return render_template('index.html', all_emails = emails)

@app.route('/process', methods=['POST'])
def email_check():
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Email is not valid!")
        return redirect('/')

    mysql = connectToMySQL('email_validation')
    emails = mysql.query_db("SELECT * FROM emails")
    print(emails)
    for item in emails:
        if request.form['email'] == item['email_address']:
            flash("Email already exists")
            return redirect('/')

    flash("You have entered a valid email address!")
    mysql = connectToMySQL('email_validation')
    query = "INSERT INTO emails (email_address, created_at, updated_at) VALUES (%(em)s, NOW(), NOW());"
    data = {
        "em": request.form['email']
    }
    new_email = mysql.query_db(query, data)
    print(new_email)
    return redirect('/success')

@app.route('/success')
def show_emails():
    mysql = connectToMySQL('email_validation')
    emails = mysql.query_db("SELECT * FROM emails")
    print(emails)
    return render_template('emails.html', emails = emails)

@app.route('/delete_email', methods=['POST'])
def delete_email():
    mysql = connectToMySQL('email_validation')
    query = "DELETE FROM emails WHERE id = %(id)s;"
    data = {
        "id": request.form['id']
    }
    mysql.query_db(query, data)
    return redirect('/success')


if __name__=="__main__":
    app.run(debug=True)