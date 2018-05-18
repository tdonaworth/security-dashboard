#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  environment {
    DC_ARGS = '-f automation/docker/test.docker-compose.yaml'
  }

  stages {
    stage('setup'){
      steps{
	// Start up the OWASP ZAP container
        sh "docker-compose $DC_ARGS up -d"

	// Install the zap-cli
	// sh "docker-compose $DC_ARGS exec -T pip install --upgrade zapcli"
	// sh "docker-compose $DC_ARGS exec -T pip install --upgrade git+https://github.com/Grunny/zap-cli.git"

	// Start ZAP on default port 8080
	// sh "docker-compose $DC_ARGS exec -T zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true"

	//
        }
    }
    stage('test'){
      steps{
        // Execute ZAP quick-scan which includes spider and active scan
	//sh "docker-compose $DC_ARGS exec -T zap-cli quick-scan 'https://sbx-iqies.hcqis.org'"
	sh "docker-compose $DC_ARGS exec -u zap -T app zap-cli quick-scan 'https://sbx-iqies.hcqis.org'"    
	//sh "docker-compose $DC_ARGS exec -T zap-cli quick-scan 'https://sbx-iqies.hcqis.org'"
        }
    }
  }
  post {
    always {
	// Bring the ZAP container down after the scan
	sh 'docker-compose -f automation/docker/test.docker-compose.yaml down'

	// Archive ZAP Report - still TBD	
    }
    success {
      echo 'alert successful build'
    }
    failure {
      echo 'alert failed build'
    }
  }
}
