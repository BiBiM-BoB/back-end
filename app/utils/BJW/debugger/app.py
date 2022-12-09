from flask import Flask, render_template, request, redirect
from flask_cors import CORS

from src.debug import debugger, pusher

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/debug', methods=['GET', 'POST'])
def debug():
    if request.method == 'POST':
        res = request.form
        debug_dict = {}

        for key, value in res.items():
            debug_dict[key] = value

        debug_dict['input_dockerfile'] = request.files.get('input_dockerfile')
        debug_dict['input_script_dir'] = request.files.getlist('input_script_dir')

        print(debug_dict)

        debugger(debug_dict)

        return 'hey'


@app.route('/push', methods=['GET', 'POST'])
def push():
    if request.method == 'POST':
        res = request.form
        push_dict = {}

        for key, value in res.items():
            push_dict[key] = value

        push_dict['input_dockerfile'] = request.files.get('input_dockerfile')
        push_dict['input_script_dir'] = request.files.getlist('input_script_dir')

        pusher(push_dict)

        return 'hey'


if __name__ == "__main__":
    app.run(debug=True)
