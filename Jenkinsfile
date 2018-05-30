#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  environment {
    OUTPUT_FILE = 'findings.html'
    TARGET_URL = 'https://sbx-iqies.hcqis.org' 
  }

  stages {
    stage('setup'){
      steps{
	// We must use ZAP stable, as bare does not have ZAP CLI
	// Bind to port 8090, override environment variable to pass health check
	sh "docker run --name zap -d -u zap -p 8090:8090 -i -e ZAP_PORT=8090 owasp/zap2docker-stable zap.sh -daemon -port 8090 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true"
	// Give the ZAP proxy server time to start
	retry(20) {
          sh 'docker exec -e ZAP_PORT=8090 zap zap-cli -p 8090 status'
        }
      }
    }
    stage('test'){
      steps{
	script {
          try {
            // Execute OWASP ZAP tests
            //sh 'docker exec zap zap-cli -p 8090 quick-scan --spider -r $TARGET_URL'
            sh 'docker exec zap zap-cli -p 8090 open-url $TARGET_URL'      
	    sh 'docker exec zap zap-cli -p 8090 active-scan -r $TARGET_URL'
	    sh 'docker exec zap zap-cli -p 8090 spider -r $TARGET_URL'
	    sh 'docker exec zap zap-cli -p 8090 ajax-spider -r $TARGET_URL'
    	  } catch (err) {
            // Problems found, but no reason to fail the build
            echo "OWASP ZAP issues security issues found!"
	    echo "Failed: ${err}"
    	  } finally {
            // Output HTML Report
            sh 'docker exec zap zap-cli -p 8090 report --output $OUTPUT_FILE --output-format html'
            sh 'docker cp zap:/zap/$OUTPUT_FILE .'
	  }
	}
      }
    }
  }
  post {
    always {
      archiveArtifacts(artifacts: OUTPUT_FILE, allowEmptyArchive: true)
      sh 'docker rm --force zap'
    }
  }
}
