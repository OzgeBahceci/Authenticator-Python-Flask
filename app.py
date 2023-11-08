from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Oz13ge24'
app.config['MYSQL_DB'] = 'db3'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = os.urandom(24)

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            if bcrypt.checkpw(password, user["password"].encode('utf-8')):
                session["name"] = user["name"]
                session["email"] = user["email"]
                session["isAdmin"] = user["isAdmin"]
                return redirect(url_for('home'))
            else:
                return "Error: Password and email do not match"
        else:
            return "Error: User not found"
    else:
        return render_template("login.html")

@app.route('/logout/', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password, isAdmin) VALUES (%s, %s, %s, %s)", (name, email, hashed_password, 0))
        mysql.connection.commit()
        session["name"] = request.form["name"]
        session["email"] = request.form["email"]
        session["isAdmin"] = 0
        return redirect(url_for('home'))

@app.route('/admin/', methods=["GET", "POST"])
def admin():
    if session.get('isAdmin') == 1:
        return render_template('admin.html')
    else:
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
