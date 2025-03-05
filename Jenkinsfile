pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }
    
    stages {
        stage('SCM') {
            steps {
                git changelog: false, poll: false, url: 'https://github.com/the-one-rvs/osteoarthritis-upchaar'
            }
        }
        stage('Build') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'dockerhubcred') {
                        sh "docker build -t quasarcelestio/osteoarthritis-upchaar:pipeline ."
                    }
                }
            }
        }
        stage('Upload image on Dockerhub') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'dockerhubcred') {
                        sh "docker push quasarcelestio/osteoarthritis-upchaar:pipeline"
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    sh "docker rmi ${DOCKER_IMAGE} || true"
                    sh "docker system prune -f || true"
                }
            }
        }
    }
}
