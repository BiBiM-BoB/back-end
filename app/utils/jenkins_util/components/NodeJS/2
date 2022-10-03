stage('Build') {
    exec('bibim-nodejs', 'npm install')
}
stage('Launch Web') {
    exec('node-test', 'npm start &')
    exec('node-test', 'sleep 1')
}