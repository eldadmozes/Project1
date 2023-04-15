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
#
import infra_flask
import os.path
import subprocess
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import boto3
import docker

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
        return f"Hello {username}!" '<br> <a href="/homepage"><button>Next</button></a>'

    return render_template("signup.html")


@app.route("/homepage")
def homepage():
    users_data = Profile.query.all()
    return render_template("homepage.html")


@app.route("/jenkins")
def jenkins():
    return render_template("jenkins.html")


@app.route('/aws')
def aws():
    return render_template('aws.html')


iam = boto3.client("iam")


@app.route('/aws_create_iam', methods=['POST', 'GET'])
def aws_create_iam():
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        iam.create_user(UserName=user_name)
        iam.add_user_to_group(GroupName='devops', UserName=user_name)
        iam.create_login_profile(UserName=user_name, Password=password, PasswordResetRequired=False)
        return f'Created successfully!'
    return render_template("aws.html")


ec2 = boto3.client("ec2")


@app.route('/aws_create_ec2', methods=['POST', 'GET'])
def aws_create_ec2():
    if request.method == 'POST':
        ec2_name = request.form.get('instance_name')
        ec2_type = request.form.get('instance_type')
        image_id = request.form.get('image_id')
        install_docker = 'install_docker' in request.form
        install_jenkins = request.form.get('install_jenkins')
        install_flask = request.form.get('install_flask')

        user_data = "#!/bin/bash\n"
        if install_docker:
            print(install_docker)
            user_data += "sudo apt-get update && sudo apt -y install docker.io\n"

            # log the user data to check if it's correct
            # print(user_data)
        # if install_jenkins:
        #     user_data += 'sudo docker pull jenkins/jenkins:lts && sudo docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts'
        # if install_flask == 'yes':
        #     user_data += 'sudo apt install python3-flask'
        # security_group = request.form.get('security_group_id')
        response = ec2.run_instances(
            ImageId=image_id,
            InstanceType=ec2_type,
            MaxCount=1,
            MinCount=1,
            KeyName='jenkins-master',
            UserData='user_data',
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{
                    'Key': 'Name',
                    'Value': ec2_name
                }]
            }]
        )
        instance_id = response['Instances'][0]['InstanceId']

        return f'Created successfully!'
    return render_template("aws.html")


@app.route("/docker", methods=["GET", "POST"])
def docker():
    if request.method == 'POST':
        image_name = request.form.get('image_name')
        subprocess.run(['docker', 'build', '-t', f'{image_name}', '.'])
        subprocess.run(['docker', 'tag', f'{image_name}', f'eldad86/project1:{image_name}'])
        subprocess.run(['docker', 'login', '-u', 'eldad86', '-p', 'Mivtzar!1961'])
        subprocess.run(['docker', 'push', f'eldad86/project1:{image_name}'])
        # subprocess.run(['docker', 'rmi', f'eldad86/project1:{image_name}'])
        return f'Docker image {image_name} created and pushed to Docker Hub'
    else:
        return render_template('docker.html')


if __name__ == "__main__":
    app.run(debug=True)
