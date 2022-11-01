# BJW
BJW는 Bibim Jenkins Wrapper의 약자로, python을 통하여 간편하게 jenkins를 다룰 수 있도록 해주는 Bibim의 custom python module입니다.

### 예시 코드(복붙용)
```python
from Interface import PipelineInterface
test = PipelineInterface('http://127.0.0.1:8080', 'admin', 'admin')

json_obj = {
    'BUILD': {
        'NodeJS': 1
    },
    'DAST': {
        'ZAP': 1, 'Arachni': 0
    },
    'SAST': {
        'CodeQL': 1
    },
    'SCA': {
        'DependencyCheck': 0, 'Dependabot': 1
    },
    'SIS': {
        'GGShield': 1, 'GitLeaks': 1
    }
}

tools_json = json.dumps(json_obj)

# create pipeline
test.createPipeline('test_pipe', 'https://github.com/johnpapa/node-hello', tools_json, '*/master', 'test_token')

# run pipeline, to see the procedure running this pipeline in pretty mode, install 'blueocean' plugin in jenkins
test.runPipeline('test_pipe')

# delete pipeline
test.deletePipeline('test_pipe')
```


###  Interface.py 사용법
 BJW의 사용자는 간편하게 디렉토리 최상단의 Interface.py를 통해 jenkins의 다양한 기능을 활용할 수 있습니다.
```python
from Interface import PipelineInterface

test = PipelineInterface('jenkinsurl', 'jenkins_id', 'jenkins_pw(or token)')
# ex: jenkinsurl = 'http://127.0.0.1:8080'

test.createPipeline(pipeline_name, git_path, tool_json, branch, build_token)
# ex: test.createPipeline('test_pipeline', 'http://github.com/example-git', tool_json, '*/master', 'testToken')

test.deletePipeline(pipeline_name)

test.runPipeline(pipeline_name)

test.modifyPipeline(미완)

pipeline_list = test.getPipelines()
# practice of PipelineInterface.getPipelines()
for pipeline in pipeline_list:
    test.deletePipeline(pipeline)
    # this deletes all pipelines

```
