from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import bcrypt
from datetime import timedelta
import pandas
from chatbotmain import get_response
import time
# Login X => session = {}
# Login O => session = {"username": "scott"}

app = Flask(__name__)
app.secret_key = "abc"
app.permanent_session_lifetime = timedelta(seconds=7200)
@app.route('/')
def index():
    isLogin = False
    if 'username' in session:
        isLogin = True
    return render_template('index.html', active_page = "index",isLogin = isLogin)
@app.route('/chatbot')
def chatbot():
    isLogin = False
    if 'username' in session:
        isLogin = True
    return render_template('chatbot.html', active_page = "consult",isLogin = isLogin)

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
            return redirect(url_for('index'))
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
    return render_template('data.html',active_page = "data", gender_distribution=gender_distribution, content_distribution=content_distribution)

@app.route('/get_response', methods=["POST"])
def get_chatbot_response():
    data = request.json
    user_input = data["message"]
    response = get_response(user_input)

    # print(response)
    return jsonify({"response": response})

@app.route('/logout', methods=["GET"])
def logout():
    session.clear() # {}
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)