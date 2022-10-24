# back-end
DevSecOps 구축 및 API 서버 구축

### notion
https://well-abrosaurus-bcd.notion.site/Back-End-7fcbd4b630b24fd5b5a97057a6cc76a5

### 구성도
<p align="center">
  <img src="https://user-images.githubusercontent.com/88534125/197490846-9c7b0048-342a-4ffc-9614-f5ef12a1cd18.png">
</p>

# app
## .env 설정
JENKINS_URL= jenkins서버의 주소가 들어감
JENKINS_ID= jenkins 서버의 ID
JENKINS_PW= jenkins 서버의 Password
BASE_JENKINS_PATH= jenkins file이 생성될 local directory path

TOKEN_SECRET_KEY= token에 사용할 secret key string
TOKEN_ALGORITHM= token 저장에 사용할 알고리즘

### .env 예시
```
JENKINS_URL="IP:PORT"
JENKINS_ID="test"
JENKINS_PW="test"
BASE_JENKINS_PATH="/home/bibim/my-jenkinsdir/"

TOKEN_SECRET_KEY="secret-key"
TOKEN_ALGORITHM="HS256"
```
