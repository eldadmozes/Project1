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
public_ip = 0





app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# db = SQLAlchemy(app)

# migrate = Migrate(app, db)


# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=False, nullable=False)
#     password = db.Column(db.String(20), unique=False, nullable=False)

#     # def __str__(self):
#     #     return f"Name:{self.first_name}, Age:{self.age}"


# @app.route("/", methods=["GET", "POST"])
# def signup():
#     # s3 = boto3.client('s3')
#     # bucket_name = "sqlabs-devops-eldadm"

#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         p = Profile(username=username, password=password)
#         db.session.add(p)
#         db.session.commit()
#         return f"Hello {username}!" '<br> <a href="/homepage"><button>Next</button></a>'

#     return render_template("signup.html")


@app.route("/homepage")
def homepage():
#     users_data = Profile.query.all()
    return render_template("homepage.html")


@app.route("/jenkins" , methods=['GET', 'POST'])
def jenkins_home():
    return render_template("jenkins.html")


@app.route('/create_jenkins_job', methods=['GET', 'POST'])
def create_jenkins_job():
    if request.method == "POST":
        job_name = request.form.get('job_test')

        # # Connect to Jenkins server
        server = jenkins.Jenkins('http://35.175.195.139:8080/', username='jenkins', password='jenkins')

        #     # Read the job configuration from the XML file
        with open('templates/jenkins_job.xml', 'r') as f:
            job_config_xml = f.read()

        #         # Create the new job with the configuration from the XML file
        server.create_job(job_name, job_config_xml)

        #Run the newly created job
        server.build_job(job_name)

        #         # Return a success message
        return 'Job created successfully!' '<br> <a href="/homepage"><button>Next</button></a>'
    return render_template("create_jenkins_job.html")


@app.route('/create_jenkins_pipeline_job', methods=['GET', 'POST'])
def create_jenkins_pipeline_job():
    if request.method == "POST":
        job_name_1 = request.form.get('job_test1')

        # # Connect to Jenkins server
        server = jenkins.Jenkins('http://35.175.195.139:8080/', username='jenkins', password='jenkins')

        #     # Read the job configuration from the XML file
        with open('templates/jenkins_job_pipeline_1.xml', 'r') as f:
            job_config_xml_1 = f.read()

        #         # Create the new job with the configuration from the XML file
        server.create_job(job_name_1, job_config_xml_1)

        #Run the newly created job
        server.build_job(job_name_1)


        #         # Return a success message
        return 'Job created successfully!' '<br> <a href="/homepage"><button>Next</button></a>'
    return render_template("create_jenkins_pipeline_job.html")






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
        return f'Created successfully!' '<br> <a href="/homepage"><button>Next</button></a>'
    return render_template("aws.html")


ec2 = boto3.client("ec2")


@app.route('/aws_create_ec2', methods=['POST', 'GET'])
def aws_create_ec2():
    global public_ip
    if request.method == 'POST':
        ec2_name = request.form.get('instance_name')
        ec2_type = request.form.get('instance_type')
        image_id = request.form.get('image_id')
        install_docker = 'install_docker' in request.form
        install_jenkins = request.form.get('install_jenkins')
        # install_flask = request.form.get('install_flask')

        user_data = "#!/bin/bash\n"
        if install_docker:
            print(install_docker)
            user_data += "sudo apt-get update && sudo apt -y install docker.io\n"
        
        time.sleep(20)   
        if install_jenkins:
            user_data += 'sudo docker pull jenkins/jenkins:lts && sudo docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts'
            # user_data += 'wget https://raw.githubusercontent.com/eldadmozes/project1/main/dev-tools/Dockerfile'
            # time.sleep(3)
            # user_data +='docker build -t jenkins .'
            # time.sleep(20)
            # user_data += 'docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins:latest'
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
        )
        instance_id = instance['Instances'][0]['InstanceId']
        print(f"Instance ID: {instance_id}")
        time.sleep(5)
        
        # retrieve the instance details using describe_instances()
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(public_ip)

        

        

        return f'Created successfully!' '<br> <a href="/homepage"><button>Homepage</button></a>'
    return render_template("aws.html")




@app.route("/docker", methods=["GET", "POST"])
def _docker():
    if request.method == 'POST':
        image_name = request.form.get('image_name')
        subprocess.run(['sudo','docker', 'build', '-t', f'{image_name}', '.'])
        subprocess.run(['sudo','docker', 'tag', f'{image_name}', f'eldad86/project1:{image_name}'])
        subprocess.run(['sudo','docker', 'login', '-u', 'eldad86', '-p', 'Mivtzar!1961'])
        subprocess.run(['sudo','docker', 'push', f'eldad86/project1:{image_name}'])
        # subprocess.run(['docker', 'rmi', f'eldad86/project1:{image_name}'])
        return f'Docker image {image_name} created and pushed to Docker Hub'
    else:
        return render_template('docker.html')


if __name__ == "__main__":
    app.run(debug=True)

