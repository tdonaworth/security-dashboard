#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  environment {
    TARGET_URL = 'https://sbx-iqies.hcqis.org/providers'
  }

  stages {
    stage('setup'){
      steps{
	// We must use ZAP stable, as bare does not have ZAP CLI
	sh "docker run --name zap -d -u zap -p 8090:8090 -i owasp/zap2docker-stable zap.sh -daemon -port 8090 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true"
	// Configure port for Docker Healthcheck, as 8080 is default
	sh 'docker exec -e ZAP_PORT=8090 zap'
	// Give the ZAP proxy server time to start
	retry(20) {
          sh 'docker exec zap zap-cli -p 8090 status'
        }
      }
    }
    stage('test'){
      steps{
	script {
          try {
            // Execute OWASP ZAP tests
            sh 'docker exec zap zap-cli -p 8090 open-url $TARGET_URL'      
	    sh 'docker exec zap zap-cli -p 8090 active-scan -r $TARGET_URL'
            sh 'docker exec zap zap-cli -p 8090 quick-scan --spider -r $TARGET_URL' 
	    sh 'docker exec zap zap-cli -p 8090 alerts -l Medium'
    	  } catch (err) {
            echo "OWASP ZAP issues security issues found!"
	    echo "Failed: ${err}"
    	  } finally {
            // Output HTML Report
            sh 'docker exec zap zap-cli -p 8090 report --output findings.html --output-format html'
            sh 'docker exec zap ls'
	  }
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
