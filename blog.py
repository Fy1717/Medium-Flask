from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    user = dict()
    user["name"] = "Furkan"
    user["surname"] = "YILDIZ"
    user["age"] = 23
    user["nick"] = "Punisher"

    return render_template('index.html', user=user)

@app.route("/about")
def about():
    return "About"

if __name__ == "__main__":
    app.run(debug=True)