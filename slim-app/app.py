import os.path
import subprocess
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import time


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/admin1/Documents/Project1/slim-app/instance/site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////project1/slim-app/instance/registered.db'


db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

    # def __str__(self):
    #     return f"Name:{self.first_name}, Age:{self.age}"


@app.route("/", methods=["GET", "POST"])
def signup():
    # s3 = boto3.client('s3')
    # bucket_name = "sqlabs-devops-eldadm"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        p = Profile(username=username, password=password)
        db.session.add(p)
        db.session.commit()
        return f"Hello {username}!" 

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

