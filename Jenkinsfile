pipeline {
  agent none
  stages {
    stage('build') {
      agent {
        docker {
          image 'squidfunk/mkdocs-material'
          args '--entrypoint=\'\''
        }

      }
      steps {
        sh 'mkdocs build'
        stash(name: 'build', includes: 'site/**/*')
      }
    }

    stage('publish') {
      agent {
        node {
          label 'local'
        }

      }
      environment {
        GITHUB_TOKEN = 'a049a1ab4ef65d3df588b68074c2dd32f9249810'
      }
      steps {
        unstash 'build'
        sh 'sudo rm -rf /var/www/remotelabz-docs || true'
        sh 'sudo mv site /var/www/remotelabz-docs'
        sh 'sudo chmod -R 755 /var/www/remotelabz-docs'
        sh 'sudo chown -R www-data:www-data /var/www/remotelabz-docs'
      }
    }

  }
}