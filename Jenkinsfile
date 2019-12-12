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
          git branch: 'master', credentialsId: 'dessa-devops-trail-rsa', url: 'git@github.com:DeepLearnI/foundations-auth-proxy.git'
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
    stage('Build and push Auth Proxy'){
      steps {
        container("python3"){
          sh 'docker login $NEXUS_DOCKER_REGISTRY -u $NEXUS_USER -p $NEXUS_PASSWORD'
          sh "./build_and_push.sh $ATLAS_TYPE"
        }
      }
    }
    stage('Pull JBoss keycloak and push auth-server'){
      steps {
        container("python3"){
          sh "docker pull jboss/keycloak:8.0.0"
          sh "docker tag jboss/keycloak:8.0.0 $NEXUS_DOCKER_REGISTRY/atlas-team/auth-server:$(python get_version.py)"
          sh "docker tag jboss/keycloak:8.0.0 $NEXUS_DOCKER_REGISTRY/atlas-team/auth-server:latest"
          sh "docker push $NEXUS_DOCKER_REGISTRY/atlas-team/auth-server"
        }
      }
    }
    stage('Trigger Atlas CE Build Pipeline') {
      steps {
        container("python3"){
          // script {
          //   echo "Triggering job for building Atlas CE Artifacts"
          //   version = sh(script: 'python get_version.py', returnStdout: true).trim()
          //   println("Attempting to trigger pipeline with version of ${version}")
          //   build job: "build-installer-atlas-ce", wait: false, parameters: [
          //     [$class: 'StringParameterValue', name: 'atlas_ce_rest_api', value: "docker-staging.shehanigans.net/atlas-ce-dev/foundations-rest-api:${version}"],
          //     [$class: 'StringParameterValue', name: 'atlas_ce_gui', value: "docker-staging.shehanigans.net/atlas-ce-dev/foundations-gui:${version}"],
          //     [$class: 'StringParameterValue', name: 'atlas_ce_tracker', value: "docker-staging.shehanigans.net/atlas-ce-dev/tracker:${version}"],
          //     [$class: 'StringParameterValue', name: 'scheduler', value: "docker-staging.shehanigans.net/atlas-ce-dev/scheduler:latest"],
          //     [$class: 'StringParameterValue', name: 'atlas_ce_worker', value: "docker-staging.shehanigans.net/atlas-ce-dev/worker:${version}"],
          //     [$class: 'StringParameterValue', name: 'archive_server', value: "docker-staging.shehanigans.net/atlas-ce-dev/archive_server:latest"],
          //     [$class: 'StringParameterValue', name: 'tensorboard_server', value: "docker-staging.shehanigans.net/atlas-ce-dev/tensorboard-server:${version}"],
          //     [$class: 'StringParameterValue', name: 'tensorboard_rest_api', value: "docker-staging.shehanigans.net/atlas-ce-dev/tensorboard-rest-api:${version}"],
          //     [$class: 'StringParameterValue', name: 'atlas_server', value: '0.2.4.dev2'],
          //     [$class: 'StringParameterValue', name: 'foundations_atlas_ce_pi_py', value: "${version}"],
          //     [$class: 'StringParameterValue', name: 'ATLAS_CE_VERSION', value: 'test_to_release']
          //   ]
          // }
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
            slackSend(channel: '#f9s-builds', attachments: attachments)
        }
    }
    success {
        slackSend color: '#00FF00', message: 'Build succeeded for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.'
    }
  }
}
