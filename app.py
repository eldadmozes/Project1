import os.path
import subprocess
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import boto3
import docker
import jenkins
import time
global public_ip
public_ip = 0





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


@app.route('/create_jenkins_job', methods=['GET', 'POST'])
def create_job():
    if request.method == "POST":
        job_name = request.form.get('job_test')

        # # Connect to Jenkins server
        server = jenkins.Jenkins('http://3.86.193.209:8080/', username='jenkins', password='jenkins')

        #     # Read the job configuration from the XML file
        with open('templates/jenkins_job.xml', 'r') as f:
            job_config_xml = f.read()

        #         # Create the new job with the configuration from the XML file
        server.create_job(job_name, job_config_xml)

        #         # Return a success message
        return 'Job created successfully!'

    return render_template("create_jenkins_job.html")



# def create_user_jenkins():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         fullname = request.form.get("fullname")
#         email = request.form.get("email")
#     # Connect to Jenkins server
#     server = jenkins.Jenkins('http://your-jenkins-server-url', username='your-jenkins-username',
#                              password='your-jenkins-api-token')
#
#     # Define the new user credentials
#     new_user = {
#         'username': 'new-user-username',
#         'password': 'new-user-password',
#         'fullName': 'New User Full Name',
#         'email': 'new.user@example.com'
#     }
#
#     # Create the new user
#     server.create_user(new_user['username'], new_user['password'], new_user['fullName'], new_user['email'])
#     return render_template("jenkins.html")


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
        if install_jenkins:
            user_data += 'sudo docker pull jenkins/jenkins:lts && sudo docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts'
        # if install_flask == 'yes':
        #     user_data += 'sudo apt install python3-flask'
        # security_group = request.form.get('security_group_id')
        instance = ec2.run_instances(
            ImageId=image_id,
            InstanceType=ec2_type,
            MaxCount=1,
            MinCount=1,
            KeyName='jenkins-master',
            UserData=user_data,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{
                    'Key': 'Name',
                    'Value': ec2_name
                }]
            }]
        )  # Note: create_instances returns a list, so we access the first (and only) element

        # instance.wait_until_running()  # Wait for the instance to start running
        # time.sleep(5)
        # instance.reload()  # Reload the instance object to get the latest information

        # public_ip = instance.public_ip_address
        # print(public_ip)
        # while response.public_ip_address is None:
        #     print("Waiting for public IP address...")
        #     time.sleep(5)
        #     response.reload()
        # instance_id = response['Instances'][0]['InstanceId']
        # time.sleep(5)
        # public_ip = response.public_ip_address
        # print(response)
        # print(public_ip)

        return f'Created successfully!'
    return render_template("aws.html")


@app.route("/docker", methods=["GET", "POST"])
def _docker():
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
