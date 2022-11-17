from flask import Flask, render_template, request, redirect
from flask_cors import CORS

from src.debug import debugger

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

        debugger(debug_dict)

        return 'hey'

if __name__ == "__main__":
    app.run(debug=True)