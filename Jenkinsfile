pipeline {
  agent any

  stages {

    stage('Clonage') {
      steps {
        git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/Azed1/mon_projet1.git'
      }
    }

    stage('Setup') {
      steps {
        sh '''
        python3 -m venv venv
        venv/bin/pip install --upgrade pip
        venv/bin/pip install -r requirements.txt
        '''
      }
    }

    stage('Tests unitaires') {
      steps {
        sh 'venv/bin/python -m pytest tests/'
      }
    }

    stage('SAST - Bandit') {
      steps {
        sh 'venv/bin/bandit -r src/ -ll'
      }
    }

    stage('Secrets Scan - Gitleaks') {
      steps {
        sh 'gitleaks detect -s . -v'
      }
    }

    stage('Docker Build + Scan') {
      steps {
        sh '''
        docker build -t mon_app:latest .
        trivy image --severity HIGH,CRITICAL mon_app:latest
        '''
      }
    }

    stage('DAST - OWASP ZAP') {
      steps {
        sh '''
        nohup venv/bin/python src/app.py > app.log 2>&1 &
        echo $! > app.pid
        sleep 5
        docker run --rm --network host ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://localhost:5000 || true
        '''
      }
    }
  }

  post {
    always {
      sh '''
      [ -f app.pid ] && kill $(cat app.pid) || true
      rm -rf venv
      '''
    }
    success {
      echo "Pipeline DevSecOps réussi"
    }
    failure {
      echo "Pipeline échoué - faille détectée"
    }
  }
}
