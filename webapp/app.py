from flask import Flask, render_template
import json

N_MAX = 30

app = Flask(__name__)

from MemDatabase import MemDatabase

# 使用示例
db = MemDatabase(data_path="/app/data/db")
db.load_data()

@app.route('/')
def home():
    tbl_ratting_movies = db.user_ratting_movies
    filter_user_id = 1345
    json_str = tbl_ratting_movies[ tbl_ratting_movies['user_id'] == filter_user_id ]  \
                .sample(n=N_MAX, random_state=42) \
                .to_json(orient='records')

    movies = json.loads(json_str)

    return render_template('movies.html', movies=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
