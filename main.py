from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from forms import GetStarted, CreateForm1, CreateForm2, ReadForm, UpdateForm, DeleteForm

app = Flask(__name__)
app.secret_key = 'bussit'
# cluster = "mongodb://atlas.."
# client = MongoClient(cluster)
client = MongoClient("localhost", 27017)
cluster = client['crud']
db = cluster.users


@app.route("/", methods=['GET', 'POST'])
def index():
    started = GetStarted()
    if started.validate_on_submit():
        return redirect(url_for('login'))
    return render_template("index.html", started=started)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    create = CreateForm1()
    login = CreateForm2()
    if create.create.data and create.validate_on_submit():
        uid = request.form['uid']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        query = {'uid': uid, 'email': email, 'password': password}
        user = db.find_one({'email': email})
        if user is not None:
            print("User already exists")
        elif password != confirm_password:
            print("Passwords don't match")
        else:
            print(uid, email, password, confirm_password)
            db.insert_one(query)
            print('User added in the Database')

    if login.login.data and login.validate_on_submit():
        print('Login')

    # if read.read.data and read.validate_on_submit():
    #     print('read')
    # if update.update.data and update.validate_on_submit():
    #     print('update')
    # if delete.delete.data and delete.validate_on_submit():
    #     print('delete')
    return render_template("login.html", create=create, login=login)


if __name__ == "__main__":
    app.run(debug=True)