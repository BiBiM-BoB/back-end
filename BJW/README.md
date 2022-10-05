# BJW
BJW는 Bibim Jenkins Wrapper의 약자로, python을 통하여 간편하게 jenkins를 다룰 수 있도록 해주는 Bibim의 custom python module입니다.

# Nodejs Inteface
 Bibim의 백엔드 아키텍쳐를 NodeJS (또는 NestJS)로 다시 설계하는 경우를 대비하여, NodeJS의 child_process를 통해 BJW에 쉽게 접근 가능하도록 하는 nodeInterface.py 또한 작성되어 있습니다.
 

###  nodeInterface.py 사용법
```javascript
spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["파일 경로/nodeInterface.py", arg1, arg2, ...]);

...
// stdout 이벤트 리스너로 실행결과 받기
pythonProcess.stdout.on('data', (data) => {
    // Do something with the data returned from python script
});

pythonProcess.stderr.on('data', (data) => {
    // Do something with the data returned from python script
});
```

