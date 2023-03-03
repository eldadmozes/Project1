properties([pipelineTriggers([githubPush()])])


pipeline {
     agent {master}
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
        stage('Cleanup') {
            steps {
                sh "rm -rf Project1"
            }
        }
        stage('Clone repo') {
            steps {
                sh "ls -la"
                sh "git clone https://github.com/eldadmozes/Project1.git"
                sh "ls -la"
            }
        }
        stage('Build') {
            steps {
                sh "docker build -t hello-web:1 ./Project1"
                sh "docker images"
            }
        }
        stage('Run image') {
            steps {
                sh "docker run -d -p 5001:5001 hello-web:1"
            }    
        }        
        stage('test') {
            steps {
                sh 'curl -I $(dig +short myip.opendns.com @resolver1.opendns.com):5001 > Result-${BUILD_USER_FIRST_NAME}-$(date -I).csv'
            }    
        }        
        stage('Stop app container') {
            steps {
                sh 'docker stop $(docker ps -q | head -n 1)'
            }
        }
        stage('Upload file to S3'){
            steps{
                withAWS(credentials:'Jenkins (AWS)', region:'us-east-1'){
                    s3Upload(bucket:'jenkins-sqlabs-eldadm',path: 'Project1/', includePathPattern:'Result*')
                }
            }
        }
    }
//    post {
//        success {
//            sh 'docker stop $(docker ps -q | head -n 1)'
//        }
//    }    
}
