stage('Copy Report') {
    sh "docker cp bibim-zap:/zap/wrk/report.json ${env.WROKSPACE}/report.json"
}