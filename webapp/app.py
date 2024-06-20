from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def home():
    movies = []
    return render_template('movies.html', movies=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
