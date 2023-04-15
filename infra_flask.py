import subprocess
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
import boto3
import docker
iam = boto3.client("iam")


def create_iam_user(user_name, password):
    response = iam.create_user(UserName=user_name)
    iam.add_user_to_group(GroupName='devops', UserName=user_name)
    iam.create_login_profile(UserName=user_name, Password=password, PasswordResetRequired=False)
    # access_key = iam.create_access_key(UserName=user_name)
    return response


