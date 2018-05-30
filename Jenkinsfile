#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  stages {
    stage('setup'){
      steps{
	// We must use ZAP stable, as bare does not have ZAP CLI
	sh "docker run --name zap -d -u zap -p 8090:8090 -i owasp/zap2docker-stable zap.sh -daemon -port 8090 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true"
	// Configure port for Docker Healthcheck
	//sh 'docker version'
	//sh 'docker exec zap sh -c "export ZAP_PORT=8090"'
	 sh 'docker exec -e ZAP_PORT=8090 zap printenv'
	sh 'docker exec zap printenv'
	// Give the ZAP proxy server time to start
	retry(20) {
          sh 'docker exec zap zap-cli -p 8090 status'
        }
      }
    }
    stage('test'){
      steps{
        try {
          sh 'docker exec zap zap-cli -p 8090 open-url https://sbx-iqies.hcqis.org'      
	  sh 'docker exec zap zap-cli -p 8090 active-scan -r https://sbx-iqies.hcqis.org'
          sh 'docker exec zap zap-cli -p 8090 quick-scan --spider -r https://sbx-iqies.hcqis.org' 
	  sh 'docker exec zap zap-cli -p 8090 alerts -l Medium'
    	} catch (err) {
          echo "Failed: ${err}"
    	} finally {
          echo "Done"
	}
      }
    }
  }
  post {
    always {
      sh 'docker rm --force zap'
      sh 'docker ps'
    }
  }
}
