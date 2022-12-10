import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from core.jenkins import Jenkins
from core.initializer.Debug_Initializer import DebugInitializer

if __name__ == "__main__":
    from ...core.jenkins import Jenkins
    from ...core.initializer.Debug_Initializer import DebugInitializer


def debugger(debug_dict):
    # create Pipeline
    jenkins = Jenkins(
        debug_dict['url'],
        debug_dict['id'],
        debug_dict['token']
    )

    initializer = DebugInitializer(debug_dict['url'])
    initializer.debug_mode(
        debug_dict['input_dockerfile'],
        debug_dict['input_script_dir']
    )

    jenkins.create_pipeline(
        debug_dict['name'],
        debug_dict['target'],
        debug_dict['target_branch'],
        groovy=debug_dict['code'],
        debug=True
    )

    pipeline = jenkins.get_pipeline(
        debug_dict['name'],
        debug_dict['target_branch']
    )

    pipeline.run()


def pusher(push_dict):
    # create Pipeline
    jenkins = Jenkins(
        push_dict['url'],
        push_dict['id'],
        push_dict['token']
    )

    debug = DebugInitializer(push_dict['url'])

    debug.jenkins_git.purge('debug')

    debug.push_mode(
        push_dict['code'],
        push_dict['groovy_name'],
        push_dict['input_dockerfile'],
        push_dict['input_script_dir'],
        push_dict['stage'],
        push_dict['tool_name']
    )

    pipeline = jenkins.get_pipeline(
        push_dict['name'],
        push_dict['target_branch']
    )

    pipeline.delete()
