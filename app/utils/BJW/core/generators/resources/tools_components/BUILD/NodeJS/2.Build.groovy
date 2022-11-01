stage('Build') {
    exec('bibim-nodejs', 'npm install')
}
stage('Launch Web') {
    exec('bibim-nodejs', 'npm start &')
    exec('bibim-nodejs', 'sleep 1')
}