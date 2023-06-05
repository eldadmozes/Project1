properties([pipelineTriggers([githubPush()])])



pipeline {
     agent {label 'slave'}
	environment {
    TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
      }
//            triggers {
//                githubPush()
    stages {
        stage('Cleanup') { agent none
            steps {
                sh "rm -rf Project1"
            }
        }
        stage('Clone repo') {
            steps {
                sh "git clone https://github.com/eldadmozes/Project1.git"
            }
        }
        stage('Build') {
            steps {
                sh "sudo docker build -t slim_app:1 . "
            }
        }
        stage('Run image') {
            steps {
                sh "sudo docker run --name slim_app -d -p 5000:5000 slim_app:1"
            }    
        }
	    stage("build user") {
  		steps{
    		wrap([$class: 'BuildUser', useGitAuthor: true]) {
      		sh 'echo ${BUILD_USER} >> Result.json'
    }
  }
}
        stage("testing") {
            steps {
                dir('/home/ubuntu/workspace/deploy-app/Project1') {
                sh 'pytest slim_app_test.py::TestClass --html=report.html'
            }
        }
    }
        stage('Stop app container') {
            steps {
                sh 'sudo docker rm slim_app -f'
            }
        }
        stage('Upload file to S3'){
            steps{
            dir ('/home/ubuntu/workspace/deploy-app/Project1'){
                withAWS(credentials:'Jenkins slave to AWS', region:'us-east-1'){
                    sh 'aws s3 cp report.html s3://sqlabs-devops-eldadm/'
                    // s3Upload(bucket:'jenkins-sqlabs-eldadm',path: 'Project1/', includePathPattern:'Result*')
                    }
                }
        // Running downstream job
		// build job: 'push image to docker hub'
            }
        }
    }
}
