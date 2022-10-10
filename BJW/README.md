# BJW
BJW는 Bibim Jenkins Wrapper의 약자로, python을 통하여 간편하게 jenkins를 다룰 수 있도록 해주는 Bibim의 custom python module입니다.

# Nodejs Inteface
 Bibim의 백엔드 아키텍쳐를 NodeJS (또는 NestJS)로 다시 설계하는 경우를 대비하여, NodeJS의 child_process를 통해 BJW에 쉽게 접근 가능하도록 하는 nodeInterface.py 또한 작성되어 있습니다.
 

###  Interface.py 사용법
```python
from Interface import PipelineInterface

PipelineInterface.createPipeline(pipeline_name, workspace_path, tool_list, branch, build_token)

PipelineInterface.deletePipeline(pipeline_name)

PipelineInterface.modifyPipeline(미완)

PipelineInterface.runPipeline(pipeline_name)
```

