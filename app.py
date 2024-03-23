from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "abc"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "test" and password == "123":
            return redirect(url_for('index'))
        flash("Wrong username or password!")
        return render_template('login.html')
    else: # method == "GET"
        return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)