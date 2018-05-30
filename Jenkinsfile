#!/usr/bin/env groovy

pipeline {
  agent {
    label 'docker-agent'
  }
  stages {
    stage('setup'){
      /*    
      agent {
        docker 'owasp/zap2docker-bare'
      }
      */
      steps{
	sh 'docker ps'
	//sh "docker run --name zap -d -u zap -p 8090:8090 -i owasp/zap2docker-stable zap.sh -daemon -port 8090 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true"
	// Use ZAP stable, as bare does not have ZAP CLI
	//sh "docker run --name zap -d -u zap -it owasp/zap2docker-stable"
	sh 'docker ps'
	//sh 'docker exec zap nohup sh -c "cd /zap && zap.sh -daemon -config api.disablekey=true" &'
	sh 'docker exec zap zap-cli -p 8090 active-scan -r https://sbx-iqies.hcqis.org'
        sh 'docker exec zap zap-cli -p 8090 quick-scan --spider -r https://sbx-iqies.hcqis.org' 
	sh 'docker exec zap zap-cli -p 8090 alerts -l Medium'
	//sh 'docker exec zap sh -c "cd /zap && ls"'
	//sh 'docker exec -w /zap zap dir'
        //sh "docker exec zap zap-cli quick-scan --spider -r http://ventera.com"
      }
    }
  }
  post {
    always {
      //sh 'docker rm --force zap'
      sh 'docker ps'
    }
    success {
      echo 'alert successful build'
    }
    failure {
      echo 'alert failed build'
    }
  }
}
