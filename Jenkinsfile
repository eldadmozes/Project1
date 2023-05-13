properties([pipelineTriggers([githubPush()])])



pipeline {
     agent {label 'slave'}
	environment {
    TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
      }
//            triggers {
//                githubPush()
    stages {
        // stage ('checkout scm'){
        //     steps {
        //         checkout([
        //             $class: 'GitSCM',
        //             branches: [[name: 'main']],
        //             userRemoteConfigs : [[
        //                 url: 'git@github.com:eldadmozes/Project1.git',
        //                 credentialsId: ''
        //                 ]]
        //             ])
        //     }
        // }
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
                sh "sudo docker build -t slim_app:1 ./Project1"
            }
        }
        stage('Run image') {
            steps {
                sh "sudo docker run -d -p 5000:5000 slim_app:1"
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
        	script {
           	STATUS = sh(script: "curl -I \$(dig +short myip.opendns.com @resolver1.opendns.com):80 | grep \"HTTP/1.1 200 OK\" | tr -d \"\\r\\n\"", returnStdout: true).trim()
            	sh 'curl -I $(dig +short myip.opendns.com @resolver1.opendns.com):5000 | grep "HTTP/1.1 200 OK" >> Result.json'
            	sh 'echo "$STATUS" >> Result.json'
			sh 'echo "${TIME}" >> Result.json'	
            	withAWS(credentials: 'JenkinsAWS', region: 'us-east-1') {
                sh "aws dynamodb put-item --table-name result --item '{\"user\": {\"S\": \"${BUILD_USER}\"}, \"date\": {\"S\": \"${TIME}\"}, \"state\": {\"S\": \"${STATUS}\"}}'"
            }
        }
    }
}
        stage('Stop app container') {
            steps {
                sh 'docker stop $(docker ps -q | head -n 1)'
		build job: 'app_deployment'
            }
        }
        // stage('Upload file to S3'){
        //     steps{
        //         withAWS(credentials:'JenkinsAWS', region:'us-east-1'){
        //             s3Upload(bucket:'jenkins-sqlabs-eldadm',path: 'Project1/', includePathPattern:'Result*')
        //         }
        //     }
        // }
    }
//    post {
//        success {
//            sh 'docker stop $(docker ps -q | head -n 1)'
//        }
//    }    
}
