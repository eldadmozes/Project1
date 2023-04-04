import boto3
import jenkins
import docker


def create_user():
    iam = boto3.client("iam")
    user_name = "my-user-test2"
    response = iam.create_user(UserName=user_name)
    response = iam.create_login_profile(
        UserName=user_name,
        Password='Password@1234',
        PasswordResetRequired=True
    )
    response = iam.add_user_to_group(
        GroupName="devops",
        UserName=user_name
    )
    response = iam.create_access_key(
        UserName=user_name
    )


def show_user_info_in_web():
    print(f"Full response: {response}")
    print(f"Access Key ID: {response['AccessKey']['AccessKeyId']}")
    print(f"Secret Access Key : {response['AccessKey']['SecretAccessKey']}")
    print("Login link: https://626685713041.signin.aws.amazon.com/console")
