
from flask import Flask, render_template, request, redirect, flash
from flask_login import login_manager, login_user, LoginManager, UserMixin, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "mysecretkey"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<email {self.email}>'


class Blogpost(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publish_date = db.Column (db.DateTime(),nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'<Blog {self.title}>'


@app.route("/layout")
def main():
    return render_template("layout.html")


@app.route("/")
def index():
    data = Blogpost.query.all()
    print(data)
    return render_template('index.html', data=data)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")

        user = User(email=email, password = password, username=username, firstname = firstname, lastname = lastname )
        db.session.add(user)
        db.session.commit()
        flash("User inserted successfully", "success")
        return redirect('/login') 

    return render_template('register.html')


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
     
        if user and password == password:
            login_user(user)
            return redirect('/')
        else:
            flash("Invalid Credentials", "warning")
            return redirect('/login')
    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return render_template('index.html')

@app.route('/blogpost', methods=['GET','POST'])
def blogpost():
    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        blogpost = Blogpost(title=title, author = author, content= content)
        db.session.add(blogpost)
        db.session.commit()
        flash("blog inserted successfully", "success")
        return redirect('/') 
    return render_template('blogpost.html')



if __name__ == "__main__":
    app.run(debug= True)

# from app import app, db
# app.app_context().push()
# db.create_all()
# from app import User
# user = User.query.all() 

### adding a user ###
# user = tablename(col1='', col2='')
# db.session.add(user)
# db.session.commit()
# data = user.query.all()
# data