# nodejs 웹 앱에 대한 jenkins ci-cd 파이프라인

$ python bibim.py
* 위의 코드만 입력하면 자동으로 
1. aws ec2가 새로 생성된다. (or 기존에 존재하던 aws ec2를 사용할 수도 있다.)
2. aws ec2에서 자동으로 docker, docker-compose 등이 설치된다.
3. 내가 테스트하고 싶은 프로젝트 폴더 경로를 지정하면, 그 폴더 내부에 있는 모든 파일이 ec2로 업로드 된다. (/home/ubuntu/bibim/)
4. docker가 생성되고, 그 docker 내부에서 지정한 여러 docker들이 또 생성된다.
5. jenkins blueocean 파이프라인이 자동으로 생성된다.
6. -- 아직 구현하지 못하였지만, jenkins-cli를 통하여 굳이 8080포트로 접속하고 수동으로 pipeline을 실행하지 않고서도 자동으로 진행된다.


이를 위해 사용자가 해야 할 일은 :
1. 필요한 경우 프로젝트 경로 내의 bibim-docker에 새로운 dockerfile을 생성한다. (zap 등)


# 실행 방법
nodejs 폴더 내부의 bibim.py를 실행하면
1. aws configure을 진행한다.
AKIAWHPSCFE22672IW6Y
7DnTCN+22Fq9xPWGsRnrR4byJiFNkraQg7TqPC8H
2. ec2를 새로 생성하고, 삭제할 것인지 / 기존에 존재하던 ec2를 사용할 것인지 정해준다. (기존에 존재하는 ec2 사용 권장)
3. 프로젝트의 경로를 지정한다. (예시 프로젝트는 nodejs-test에 들어있다.)
4. Bibimfile의 경로를 지정한다. (bibim.py가 들어있는 폴더 내부에 있다.)
5. 어찌어찌 진행되면, 브라우저로 aws 8080포트에 접속하여 blueocean pipeline을 실행한다.
