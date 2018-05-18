#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  environment {
    TARGET_URL=https://sbx-iqies.hcqis.org/
  }

  stages {
    stage('setup'){
      steps{
	// Start up the OWASP ZAP container
	CONTAINER_ID=$(docker run -u zap -p 2375:2375 -d owasp/zap2docker-weekly zap.sh -daemon -port 2375 -host 127.0.0.1 -config api.disablekey=true -config scanner.attackOnStart=true -config view.mode=attack -config connection.dnsTtlSuccessfulQueries=-1 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true)
        }
    }
    stage('test'){
      steps{
	sh "docker ps"
        docker exec $CONTAINER_ID zap-cli -p 2375 status -t 120 && docker exec $CONTAINER_ID zap-cli -p 2375 open-url $TARGET_URL
	docker exec $CONTAINER_ID zap-cli -p 2375 spider $TARGET_URL
	docker exec $CONTAINER_ID zap-cli -p 2375 active-scan -r $TARGET_URL
	docker exec $CONTAINER_ID zap-cli -p 2375 alerts
        }
    }
  }
  post {
    always {
	// Bring the ZAP container down after the scan
	docker logs $CONTAINER_ID
	docker stop $CONTAINER_ID	
    }
    success {
      echo 'alert successful build'
    }
    failure {
      echo 'alert failed build'
    }
  }
}
