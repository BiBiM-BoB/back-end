stage('Run NodeJS Docker') {
    def nodejs_img = docker.image('node:lts-alpine')
    
    try { 
        def nodejs_container = nodejs_img.run("-dt --rm -p 3000:3000 -w /app/src -v ${env.WORKSPACE}:/app/src --name bibim-nodejs")
    } catch {
        echo "Don't worry, program is in good status."
        stop_container('bibim-nodejs')
        def nodejs_container = nodejs_img.run("-dt --rm -p 3000:3000 -w /app/src -v ${env.WORKSPACE}:/app/src --name bibim-nodejs")
    } 
}