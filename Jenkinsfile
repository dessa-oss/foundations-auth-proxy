def build_number = env.BUILD_URL
def customMetrics = [:]
def customMetricsMap = [:]

pipeline{
  agent {
    label 'ci-pipeline-jenkins-slave'
  }
  stages {
    stage('Preparation') {
      steps {
        container("python3") {
          git branch: 'master', credentialsId: 'dessa-devops-trail-rsa', url: 'git@github.com:dessa-research/foundations-auth-proxy.git'
        }
      }
    }
    stage('Install Requirements') {
      steps {
        container("python3") {
          sh "pip install -r requirements.txt"
        }
      }
    }
    stage('Build Auth Proxy') {
      steps {
        container("python3") {
          sh "./build_dist.sh"
        }
      }
    }
    stage('Run Tests') {
      steps {
        container("python3") {
          sh "echo 'No test available'"
        }
      }
    }
    stage('Setup Docker Credentails') {
      steps {
        container("python3") {
          sh 'docker login $NEXUS_DOCKER_STAGING -u $NEXUS_USER -p $NEXUS_PASSWORD'
        }
      }
    }
    stage('Build Auth Proxy for Atlas'){
      steps {
        container("python3") {
          sh "DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/atlas ./build_image.sh null"
          sh "DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/atlas-team ./build_image.sh"
        }
      }
    }
    stage('Push Auth Proxy for Atlas'){
      steps {
        container("python3") {
          sh "DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/atlas ./push_image.sh"
          sh "DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/atlas-team ./push_image.sh"
        }
      }
    }
    stage('Build Auth Proxy for Orbit'){
      steps {
        container("python3") {
          sh "DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/orbit-team ./build_image.sh"
        }
      }
    }
    stage('Push Auth Proxy for Orbit'){
      steps {
        container("python3") {
          sh "DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/orbit-team ./push_image.sh"
        }
      }
    }
    stage("Calculate Recovery Metrics") {
      steps {
        script {
          def last_build = currentBuild.getPreviousBuild()
          def last_failed_build
          def current_time = System.currentTimeMillis()

          while(last_build != null && last_build.result == "FAILURE") {
            last_failed_build = last_build
            last_build = last_build.getPreviousBuild()
          }

          if(last_failed_build != null) {
            time_to_recovery = current_time - last_failed_build.getTimeInMillis()
            customMetrics["time_to_recovery"] = time_to_recovery
          }
        }
      }
    }
  }
  post {
    always {
      script {
            customMetricsMap["jenkins_data"] = customMetrics
      }
      influxDbPublisher selectedTarget: 'foundations', customPrefix: 'foundations', customProjectName: 'foundations', jenkinsEnvParameterField: '', jenkinsEnvParameterTag: '', customDataMap: customMetricsMap
    }
    failure {
        script {
            def output_logs = String.join('\n', currentBuild.rawBuild.getLog(200))
            def attachments = [
                [
                    pretext: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                    text: output_logs,
                    fallback: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                    color: '#FF0000'
                ]
            ]
            slackSend(channel: '#dessa-atlas-builds', attachments: attachments)
        }
    }
    success {
        slackSend color: '#00FF00', message: 'Build succeeded for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.'
    }
  }
}
