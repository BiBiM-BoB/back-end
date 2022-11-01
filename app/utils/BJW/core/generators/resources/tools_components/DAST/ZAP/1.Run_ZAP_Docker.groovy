stage('Run ZAP Docker') {
    def zap_img = docker.image('owasp/zap2docker-stable')
    
    try { 
        def zap_container = zap_img.run("-dt --rm --name bibim-zap")
    } catch(error) {
        stop_container('bibim-zap')
        echo "Don't worry, program is in good status."
        def zap_container = zap_img.run("-dt --rm --name bibim-zap")
    } 
}