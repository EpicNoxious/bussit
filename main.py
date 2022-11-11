from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from pymongo import MongoClient
from forms import GetStarted, Register, Login, ReadForm, UpdateForm, DeleteForm

app = Flask(__name__)
app.secret_key = 'Bussit'
# cluster = "mongodb://atlas.."
# client = MongoClient(cluster)
client = MongoClient("localhost", 27017)
cluster = client['crud']
db = cluster.users


# USER
class User:
    def begin_session(self, user):
        del user['_id']
        del user['password']
        print(user)
        session['logged_in'] = True
        session['user'] = user
        print('Session started successfully')

    def end_session(self):
        session.clear()
        return redirect("/")

    def register(self, query):
        user = {
            "uid": query['uid'],
            "email": query['email'],
            "password": query['password'],
            }
        db.insert_one(user)
        print('User added in the Database')
        return self.begin_session(user)

    def login(self, profile):
        user = {
            "_id": profile['_id'],
            "uid": profile['uid'],
            "email": profile['email'],
            "password": profile['password'],
            }
        return self.begin_session(user)


@app.route("/", methods=['GET', 'POST'])
def index():
    started = GetStarted()
    if started.validate_on_submit():
        return redirect(url_for('signin'))
    return render_template("index.html", started=started)


@app.route("/login/", methods=['GET', 'POST'])
def signupin():
    register = Register()
    login = Login()
    user = User()

    # User Sign Up
    if register.register.data and register.validate():
        uid = request.form['uid']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        query = {
            'uid': uid,
            'email': email,
            'password': password
            }
        profile = db.find_one({'uid': uid})

        if profile is not None:
            print("User already exists")
            flash('User already exists')
        elif password != confirm_password:
            print("Passwords don't match")
            flash("Passwords don't match")
        else:
            user.register(query)
            return redirect(url_for('success'))

    # User Sign In
    if login.login.data and login.validate():
        uid = request.form['uid']
        password = request.form['password']

        profile = db.find_one({'uid': uid})
        print(profile)

        if profile is None:
            print("User does not exist in database")
            flash("User does not exist in database")
        elif password != profile['password']:
            print("Passwords don't match")
            flash("Passwords don't match")
        else:
            user.login(profile)
            return redirect(url_for('success'))

    # if read.read.data and read.validate_on_submit():
    #     print('read')
    # if update.update.data and update.validate_on_submit():
    #     print('update')
    # if delete.delete.data and delete.validate_on_submit():
    #     print('delete')
    return render_template("signupin.html", register=register, login=login)


@app.route("/session/", methods=['GET', 'POST'])
def success():
    return render_template('session.html')

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    register = Register()
    user = User()
    if register.register.data and register.validate():
        uid = request.form['uid']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        query = {
            'uid': uid,
            'email': email,
            'password': password
            }
        profile = db.find_one({'uid': uid})

        if profile is not None:
            print("User already exists")
            flash("User already exists")
            flash("User already exists")
        elif password != confirm_password:
            print("Passwords don't match")
            flash("Passwords don't match")
        else:
            user.register(query)
            return redirect(url_for('success'))

    return render_template('signuppage.html', register=register)


@app.route("/signin/", methods=['GET', 'POST'])
def signin():
    login = Login()
    user = User()
    if login.login.data and login.validate():
        uid = request.form['uid']
        password = request.form['password']

        profile = db.find_one({'uid': uid})
        print(profile)

        if profile is None:
            print("User does not exist in database")
            flash("User does not exist in database")
        elif password != profile['password']:
            print("Passwords don't match")
            flash("Passwords don't match")
        else:
            user.login(profile)
            return redirect(url_for('success'))
    return render_template('signinpage.html', login=login)


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)
