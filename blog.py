#!/usr/local/bin/python

#- * -coding: utf - 16 - * -

# -------------------------------------------- IMPORT AREA --------------------------------------------------------
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
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

# ------------------------------------------  LOGIN FORM -------------------------------------------------------
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")
# -----------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "hwblog"

# ------------------------------------------ MYSQL CONNECTION -----------------------------------------------------
app.config["MYSQL_HOST"] = "frknyldz.site"
app.config["MYSQL_USER"] = "frknyldz21_fy"
app.config["MYSQL_PASSWORD"] = "furkan123."
app.config["MYSQL_DB"] = "frknyldz21_hwblog"
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

# LOGIN DECORATOR -------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Öncelikle giriş yapmanız gerekiyor", "danger")
            return redirect(url_for("login"))
    
    return decorated_function

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
        password = form.password.data

        cursor = mysql.connection.cursor()

        sorgu = "Insert into users(name, email, username, password) VALUES(%s, %s, %s, %s)"

        cursor.execute(sorgu,(name, email, username, password))

        mysql.connection.commit()

        cursor.close()

        flash("KAYIT BAŞARILI..", "success")

        return redirect(url_for("login"))
    else:
        return render_template("register.html", form = form)
# -----------------------

# LOGIN -----------------
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST":
        username = form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "Select * From users where username = %s"

        result = cursor.execute(sorgu, (username,))

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]

            if password == real_password:
                flash("Giriş Başarılı..", "success")

                session["logged_in"] = True
                session["username"] = username
                
                return redirect(url_for("index"))
            else:
                flash("Kullanıcı Bilgilerini Kontrol Ediniz..", "danger")

                return redirect(url_for("login"))

        else:
            flash("Kullanıcı Bulunamadı..", "danger")

            return redirect(url_for("login"))


    return render_template("login.html", form = form)
# -----------------------

# LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("index"))
# -----------------------

# DASHBOARD -------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
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