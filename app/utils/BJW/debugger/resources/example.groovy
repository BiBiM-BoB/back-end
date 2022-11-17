def stop_container(container_name) {
    sh 'docker stop ' + container_name
}

def exec(container_name, command) {
    try {
        def cmd = 'docker exec ' + container_name + ' ' + command
        sh cmd
    } catch(error) {
        stop_container(container_name)
    }
}

node {
    stage('Run NodeJS Docker') {
        def nodejs_img = docker.image('node:lts-alpine')
        
        try { 
            def nodejs_container = nodejs_img.run("-dt --rm -p 3000:3000 -w /app/src -v ${env.WORKSPACE}:/app/src --name bibim-nodejs")
        } catch(error) {
            echo "Don't worry, program is in good status."
            stop_container('bibim-nodejs')
            def nodejs_container = nodejs_img.run("-dt --rm -p 3000:3000 -w /app/src -v ${env.WORKSPACE}:/app/src --name bibim-nodejs")
        } 
    }
    stage('Build') {
        exec('bibim-nodejs', 'npm install')
    }
    stage('Launch Web') {
        exec('bibim-nodejs', 'npm start &')
        exec('bibim-nodejs', 'sleep 1')
    }
}