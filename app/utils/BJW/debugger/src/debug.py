import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from core.pipeline import Pipeline

def debugger(debug_dict):
    # create Pipeline
    pipe = Pipeline(
        debug_dict['url'], 
        debug_dict['id'], 
        debug_dict['token'],
        debug_dict['name']
    )

    pipe.create_pipeline_by_raw_groovy(
        debug_dict['code'], 
        debug_dict['target'], 
        debug_dict['target_branch']
    )

    pipe.run_pipeline()