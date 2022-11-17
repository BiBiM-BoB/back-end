import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from core.pipeline import Pipeline

if __name__ == "__main__":
    from ...core.pipeline import Pipeline


def debugger(debug_dict):
    # create Pipeline
    pipe = Pipeline(
        debug_dict['url'],
        debug_dict['id'],
        debug_dict['token'],
        debug_dict['name'],
        'DEBUG',
        input_dockerfile=debug_dict['input_dockerfile'],
        input_script_dir=debug_dict['input_script_dir']
    )

    pipe.create_pipeline_by_raw_groovy(
        debug_dict['code'],
        debug_dict['target'],
        debug_dict['target_branch']
    )

    pipe.run_pipeline()


def pusher(push_dict):
    # create Pipeline
    pipe = Pipeline(
        push_dict['url'],
        push_dict['id'],
        push_dict['token'],
        push_dict['name'],
        'PUSH',
        code=push_dict['code'],
        groovy_name=push_dict['groovy_name'],
        input_dockerfile=push_dict['input_dockerfile'],
        input_script_dir=push_dict['input_script_dir'],
        stage=push_dict['stage'],
        tool_name=push_dict['tool_name']
    )
