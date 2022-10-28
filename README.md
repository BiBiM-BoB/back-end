# back-end
DevSecOps 구축 및 API 서버 구축

### notion
https://well-abrosaurus-bcd.notion.site/Back-End-7fcbd4b630b24fd5b5a97057a6cc76a5

### 구성도
<p align="center">
  <img src="https://user-images.githubusercontent.com/88534125/197490846-9c7b0048-342a-4ffc-9614-f5ef12a1cd18.png">
</p>

# Git
## 커밋 컨벤션(commit convention)
https://well-abrosaurus-bcd.notion.site/github-e90a044191dd4d2dabe0a78453868a98

## Branch
```
main: 최종 동작 소스코드 브랜치.(문제없이 실행되어야함)
develop: 개발을 하기 위한 브랜치.(기본적으로 여기에서 작업하시면 됩니다)
```

# app
## 실행 하기 위한 구성
### .env 설정
```
JENKINS_URL= jenkins서버의 주소가 들어감
JENKINS_ID= jenkins 서버의 ID
JENKINS_PW= jenkins 서버의 Password
BASE_JENKINS_PATH= jenkins file이 생성될 local directory path

TOKEN_SECRET_KEY= token에 사용할 secret key string
TOKEN_ALGORITHM= token 저장에 사용할 알고리즘
LOGGING_PATH= 로그가 저장될 디렉토리 경로(자세한건 app의 __init__ 참조)
```

### .env 예시
```
JENKINS_URL="IP:PORT"
JENKINS_ID="test"
JENKINS_PW="test"
BASE_JENKINS_PATH="/home/bibim/my-jenkinsdir/"

TOKEN_SECRET_KEY="secret-key"
TOKEN_ALGORITHM="HS256"
LOGGING_PATH="/home/bibim/back-end/app/"
```

### logs 디렉토리 생성 및 .log파일 생성
LOGGING_PATH에 해당하는 위치에 logs 디렉토리를 생성 후, bibim.app.log 파일을 생성해야 함.
