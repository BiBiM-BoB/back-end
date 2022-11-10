docker run -d --name jenkins \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v jenkins:/var/jenkins_home \
    -p 8080:8080 bibim-jenkins:0.1