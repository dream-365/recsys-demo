from flask import Flask, render_template
import json
import numpy as np
import faiss

N_MAX = 30
TOP_N = 100

app = Flask(__name__)

from MemDatabase import MemDatabase

# 使用示例
db = MemDatabase(data_path="/app/data/db")
db.load_data()

item_embs = np.load("/app/model/item_embs.npy")
user_embs = np.load("/app/model/user_embs.npy")
user_id_idx = np.load("/app/model/user_id_idx.npy")
movie_id_idx = np.load("/app/model/movie_id_idx.npy")

embedding_dim = 64

# 构建user_id和embedding的KV
user_id_emb_dict = {}

for index, value in enumerate(user_id_idx):
    user_id_emb_dict[user_id_idx[index]] = user_embs[index]

# 加载所有的item 构建user_id和embedding的KV
faiss_index = faiss.IndexFlatIP(embedding_dim)
faiss_index.add(item_embs)

@app.route('/')
def home():
    tbl_ratting_movies = db.user_ratting_movies
    tbl_movies = db.movies

    filter_user_id = 1024
    json_str = tbl_ratting_movies[ tbl_ratting_movies['user_id'] == filter_user_id ]  \
                .sample(n=N_MAX, random_state=42) \
                .to_json(orient='records')
    watched_movies = json.loads(json_str)
    
    user_emb_query = [ user_id_emb_dict[filter_user_id] ]
    D, I = faiss_index.search(np.ascontiguousarray(user_emb_query), TOP_N)
    search_idx_result = I[0]
    retrival_movie_ids = []

    for idx in search_idx_result:
        retrival_movie_ids.append(movie_id_idx[idx])

    json_str = tbl_movies[tbl_movies['movie_id'].isin(retrival_movie_ids)]  \
                        .to_json(orient='records')
    
    retrival_movies = json.loads(json_str)

    return render_template('movies.html', 
                           watched_movies=watched_movies, 
                           retrival_movies=retrival_movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
