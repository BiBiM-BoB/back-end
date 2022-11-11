sudo docker run -d --name jenkins -v /var/run/docker.sock:/var/run/docker.sock -v -e "-Djenkins.install.runSetupWizard=false" jenkins:/var/jenkins_home -p 8080:8080 bibim-jenkins:0.1
