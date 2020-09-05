#!/usr/local/bin/python

#- * -coding: utf - 16 - * -

# -------------------------------------------- IMPORT AREA --------------------------------------------------------
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
# -----------------------------------------------------------------------------------------------------------------


# ------------------------------------------  REGISTER FORM -------------------------------------------------------
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(min=4, max=30)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=4, max=30)])
    email = StringField("Email Adresi", validators=[validators.Email(message="Geçerli bir email adresi girin")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message= "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname= "confirm", message= "Yanlış Parola")])
    confirm = PasswordField("Parola Doğrula")
# -----------------------------------------------------------------------------------------------------------------

app = Flask(__name__)

# ------------------------------------------ MYSQL CONNECTION -----------------------------------------------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "hwblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
# -----------------------------------------------------------------------------------------------------------------

# ------------------------------------------ PAGE ROUTES FUNCTIONS ------------------------------------------------

# MAIN ------------------
@app.route("/")
def index():
    educations = ["Flutter", "Python", "Xamarin", "Javascript", "Firebase"]

    instructors = [{
        "id": 1,
        "name": "Furkan YILDIZ",
        "profession": "PYTHON"
    }, {
        "id": 2,
        "name": "Kadriye MACIT",
        "profession": "FLUTTER"
    }, {
        "id": 3,
        "name": "Beyza INCE",
        "profession": "ARTIFICAL INTELLIGENCE"
    }, {
        "id": 4,
        "name": "Oguz DEMIR",
        "profession": "JAVASCRIPT"
    }, {
        "id": 5,
        "name": "Alp YURTSEVEN",
        "profession": "ASP .NET"
    }]

    return render_template("index.html", instructors=instructors, educations=educations)
# -----------------------

# ABOUT -----------------
@app.route("/about")
def about():
    return render_template("about.html")
# -----------------------

# REGISTER --------------
@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        ''' cursor = mysql.connection.cursor()

        sorgu = "Insert into users(name, email, username, password) VALUES(%s, %s, %s, %s)"

        cursor.execute(sorgu,(name, email, username, password))

        mysql.connection.commit()

        cursor.close()'''

        print('------>>>>>' + cursor)

        return redirect(url_for("index"))
    else:
        return render_template("register.html", form = form)
# -----------------------

# LOGIN -----------------
@app.route("/login")
def login():
    return render_template("login.html")
# -----------------------

# EDUCATIONS ------------
@app.route("/educations")
def educations():
    return render_template("educations.html")
# -----------------------

# DETAIL ----------------
@app.route("/instructors/<string:id>")
def detail(id):
    return "Instructor " + id 
# -----------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug = True)