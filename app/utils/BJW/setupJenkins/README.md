# INSTALL AND RUN JENKINS
 현재 디렉터리의 setup.py를 실행하여 Docker out of Docker 아키텍쳐의 젠킨스를 편리하게 설치할 수 있다.
 
 다음의 세가지 모드를 지원한다.
 1. 로컬에 jenkins 설치
 2. ec2에 jenkins 설치 (AWS configure을 직접 진행해야 함 -> 키를 모를 경우 강한승 멘티에게 말해주세요.)
 3. ssh를 통하여 jenkins 설치

 추가적으로 다음의 용도로 사용될 수 있다.
 1. ./script/Manager/AWSManager 을 통해 쉽게 AWS와 관련된 작업 진행 (EC2 생성 등 -> 주석 참고)
 2. ./script/Manager/SSHManager 을 통해 SSH와 관련된 다양한 기능을 활용
 3. 추후 bibim 프로젝트 사용자가, 복잡한 설치 과정 없이 원하는 곳에 Docker out of docker 형태의 Jenkins 설치

# IF trouble occured...
 설치 과정에서 예상치 못한 문제가 발생하여 과정이 중단된 경우.. 
 2, 3번 모드를 사용한 경우 이미 sftp file upload는 진행되었을 가능성이 매우 크다. 따라서 직접 ssh로 접속하여 /home/ubuntu/setup/ 디렉터리 내부의 setup.sh 및 run.sh를 실행시키면 된다.