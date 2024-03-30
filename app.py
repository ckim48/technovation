from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import bcrypt
from datetime import timedelta
import pandas

# Login X => session = {}
# Login O => session = {"username": "scott"}

app = Flask(__name__)
app.secret_key = "abc"
app.permanent_session_lifetime = timedelta(seconds=7200)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()
        command = "SELECT password FROM Users WHERE username = ?;"
        cursor.execute(command, (username,))
        result = cursor.fetchone()[0]
        password = password.encode("UTF-8")
        if bcrypt.checkpw(password, result):
            session["username"] = username  #session = {"username": "scott"}
            return redirect(url_for('data'))
        flash("Wrong username or password!")
        return render_template('login.html')
    else: # method == "GET"
        return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        age = request.form.get("age")
        gender = request.form.get("gender")

        # Connecting(Accessing) with our DB
        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()

        command = "SELECT password FROM Users WHERE username = ?;"
        cursor.execute(command, (username,)) # username = scott123
        result = cursor.fetchone() # None
        if result is None:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            command = "INSERT INTO Users (username, password, age, gender) VALUES (?,?,?,?);"
            cursor.execute(command, (username, hashed_password, age, gender))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            flash("Existing Username")
            return render_template('register.html')
    else:
        return render_template('register.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    data = pandas.read_csv("consulting_data_content_logic.csv")
    gender_distribution = data["gender"].value_counts().to_dict()
    content_distribution = data["type_of_consulting"].value_counts().to_dict()
    return render_template('data.html', gender_distribution=gender_distribution, content_distribution=content_distribution)




if __name__ == '__main__':
    app.run(debug=True)