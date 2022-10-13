stage('Execute ZAP') {
    exec('bibim-zap', 'mkdir /zap/wrk')
    exec('bibim-zap', 'zap-full-scan.py -t http://112.167.178.26:3000 -J /zap/wrk/report.json')
}