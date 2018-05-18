#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  environment {
    TARGET_URL='https://sbx-iqies.hcqis.org'
    CONTAINER_NAME='zap'
  }

  stages {
    stage('setup'){
      steps{
	// Start up the OWASP ZAP container
	//CONTAINER_ID=$(sh "docker run -u zap -p 2375:2375 -d owasp/zap2docker-weekly zap.sh -daemon -port 2375 -host 127.0.0.1 -config api.disablekey=true -config scanner.attackOnStart=true -config view.mode=attack -config connection.dnsTtlSuccessfulQueries=-1 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true")
	//CONTAINER_ID=$(sh "docker run -u zap -p 2375:2375 -d owasp/zap2docker-weekly zap.sh -daemon -port 2375 -host 127.0.0.1")
	sh "docker run -u zap -p 2375:2375 -d owasp/zap2docker-bare zap.sh -daemon -port 2375 -host 127.0.0.1 --name $CONTAINER_NAME"
        }
    }
    stage('test'){
      steps{
	sh "docker ps" 
        sh "docker exec -d zap zap-cli -p 2375 status -t 120 && docker exec $CONTAINER_ID zap-cli -p 2375 open-url $TARGET_URL"
	sh "docker exec -d zap zap-cli -p 2375 spider $TARGET_URL"
	sh "docker exec -d zap zap-cli -p 2375 active-scan -r $TARGET_URL"
	sh "docker exec -d zap zap-cli -p 2375 alerts"
        }
    }
  }
  post {
    always {
	// Bring the ZAP container down after the scan
	sh "docker logs $CONTAINER_NAME"
	sh "docker stop $CONTAINER_NAME"	
    }
    success {
      echo 'alert successful build'
    }
    failure {
      echo 'alert failed build'
    }
  }
}
