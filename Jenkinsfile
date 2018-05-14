#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  environment {
    DC_ARGS = '-f automation/docker/test.docker-compose.yaml'
    REGISTRY = 'nexus.hcqis.org:28446'
    // TODO: change this to pull from config
    SERVICE_NAME = 'example'
    CLUSTER = 'cms-iqies-microservices'
  }

  stages {
    stage('setup'){
      steps{
        script {
          env.GIT_COMMIT_SHORT = sh(script: "echo ${env.GIT_COMMIT} | cut -c 1-7", returnStdout: true).trim()
        }
        sh "docker-compose $DC_ARGS up -d --build"
      }
    }
    stage('test'){
      steps {
        // Use CMS Nexus
        sh "docker-compose $DC_ARGS exec -T app yarn config set registry http://nexus.hcqis.org:8081/repository/iqies-npm/"
        // Lint, test, and code coverage
        sh "docker-compose $DC_ARGS exec -T app yarn lint"
        sh "docker-compose $DC_ARGS exec -T app yarn coverage"
        sh "docker-compose $DC_ARGS exec -T app yarn exec nyc check-coverage -- --lines 75"
        // Security
        // NSP
        sh "docker-compose $DC_ARGS exec -T app yarn global add nsp"
        sh "docker-compose $DC_ARGS exec -T app nsp check --proxy $HTTPS_PROXY"
        // Retire.js
        sh "docker-compose $DC_ARGS exec -T app yarn global add retire"
        sh "docker-compose $DC_ARGS exec -T app retire --proxy $HTTPS_PROXY"
      }
    }
    stage('build'){
      when {
        branch 'develop'
      }
      environment {
        NODE_ENV = 'production'
      }
      steps {
        withCredentials(
          [usernamePassword(credentialsId: 'iqies-devops-resource',
            usernameVariable: 'USER',
            passwordVariable: 'PASS'),
          string(credentialsId: 'iQIES-root-RDS-connectionstring',
            variable: 'DATABASE_URL')
          ]
        ){
          // TODO: tagging strategy, only tagging with latest currently
          sh "docker login -u $USER -p $PASS $registry"
          sh "docker build -t $REGISTRY/$SERVICE_NAME:$GIT_COMMIT_SHORT --build-arg DATABASE_URL=$DATABASE_URL --build-arg SERVICE_NAME=$SERVICE_NAME -f automation/docker/build.Dockerfile ."
          sh "docker push $REGISTRY/$SERVICE_NAME"
        }
      }
    }
    stage('deploy'){
      when {
        branch 'develop'
      }
      agent {
        label 'sshpass-docker'
      }
      steps {
        withCredentials(
          [usernamePassword(credentialsId: 'iqies-devops-resource',
          usernameVariable: 'USER',
          passwordVariable: 'PASS')]
        ){
          sh "sed -e 's/%REGISTRY%/$REGISTRY/g' -e 's/%SERVICE_NAME%/$SERVICE_NAME/g' -e 's/%IMAGE_TAG%/$GIT_COMMIT_SHORT/g' automation/docker/deploy.docker-compose.yml > docker-compose.yml"
          sh "cat automation/docker/deploy.ecs-params.yml | sshpass -p $PASS ssh -v -o StrictHostKeyChecking=No -l \"qnet\\$USER\" 10.137.177.149 \"cat - > ecs-params.yml\""
          sh "cat docker-compose.yml | sshpass -p $PASS ssh -v -o StrictHostKeyChecking=No -l \"qnet\\$USER\" 10.137.177.149 \"cat - > docker-compose.yml\""
          sh "sshpass -p $PASS ssh -o StrictHostKeyChecking=no -l \"qnet\\$USER\" 10.137.177.149 ecs-cli compose -p $SERVICE_NAME -c $CLUSTER service up --timeout 8 --launch-type EC2"
        }
      }
      post {
        always {
          archiveArtifacts(artifacts: 'docker-compose.yml', allowEmptyArchive: true)
        }
      }
    }
  }
  post {
    always {
      archiveArtifacts(artifacts: 'yarn-error.log', allowEmptyArchive: true)
      sh 'docker-compose -f automation/docker/test.docker-compose.yaml down'
      deleteDir()
    }
    success {
      echo 'alert successful build'
    }
    failure {
      echo 'alert failed build'
    }
  }
}
