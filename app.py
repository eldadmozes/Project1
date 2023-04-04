# import os.path
# from flask import Flask, request, redirect
# from flask.templating import render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, migrate
# import boto3
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# app.config['MAX_CONTENT'] = 16 * 1024 * 1024
# ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg", "gif"]
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# db = SQLAlchemy(app)
#
# migrate = Migrate(app, db)
#
#
# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(20), unique=False, nullable=False)
#     last_name = db.Column(db.String(20), unique=False, nullable=False)
#     age = db.Column(db.Integer, unique=False, nullable=False)
#     picture = db.Column(db.String(100), unique=False, nullable=True)
#
#     def __str__(self):
#         return f"Name: {self.first_name}, Age:{self.age}"
#
#
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     s3 = boto3.client('s3')
#     bucket_name = "jenkins-sqlabs-eldadm"
#     key_name = "download.png"
#     if request.method == "POST":
#         first_name = request.form.get("fname")
#         last_name = request.form.get("lname")
#         age = request.form.get("age")
#         file = request.files.get("filename")
#         if allowed_file(file.filename):
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             s3.upload_file(file_path, bucket_name, key_name)
#             p = Profile(first_name=first_name, last_name=last_name, age=age, picture=file.filename)
#             db.session.add(p)
#             db.session.commit()
#         return f"{first_name} {last_name} {age}"
#     return render_template("signup.html")
#
#
# @app.route("/homepage")
# def homepage():
#     users_data = Profile.query.all()
#     return render_template("homepage.html", users_data=users_data)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


import os.path
from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import boto3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)


    # def __str__(self):
    #     return f"Name:{self.first_name}, Age:{self.age}"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # s3 = boto3.client('s3')
    # bucket_name = "sqlabs-devops-eldadm"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # p = Profile(username=username, password=password)
        # db.session.add(p)
        # db.session.commit()
        return f"hello {username}!"

    return render_template("signup.html")


@app.route("/homepage")
def homepage():
    users_data = Profile.query.all()
    return render_template("homepage.html", users_data=users_data)


if __name__ == "__main__":
    app.run(debug=True)
