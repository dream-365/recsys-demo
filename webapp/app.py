from flask import Flask, render_template
import json
import numpy as np
import faiss
from MemDatabase import MemDatabase

LAST_N = 30
TOP_N = 100
embedding_dim = 32

app = Flask(__name__)

# 初始化数据库
def initialize_database():
    db = MemDatabase(data_path="/app/data/db")
    db.load_data()
    return db

# 加载嵌入向量和索引
def load_embeddings():
    item_embs = np.load("/app/model/item_embs.npy")
    user_embs = np.load("/app/model/user_embs.npy")
    user_id_idx = np.load("/app/model/user_id_idx.npy")
    movie_id_idx = np.load("/app/model/movie_id_idx.npy")
    return item_embs, user_embs, user_id_idx, movie_id_idx

# 构建 user_id 和嵌入向量的字典
def build_user_emb_dict(user_id_idx, user_embs):
    return {user_id: user_emb for user_id, user_emb in zip(user_id_idx, user_embs)}

# 初始化 FAISS 索引
def initialize_faiss(item_embs, embedding_dim):
    faiss_index = faiss.IndexFlatIP(embedding_dim)
    faiss_index.add(item_embs)
    return faiss_index

# 根据用户ID获取用户嵌入向量
def get_user_emb(user_id_emb_dict, user_id):
    return np.ascontiguousarray([user_id_emb_dict[user_id]])

# 在 FAISS 索引中搜索前 N 个电影
def search_top_n_movies(faiss_index, user_emb_query, N):
    D, I = faiss_index.search(user_emb_query, N)
    return I[0]

# 获取用户观看过的电影
def get_watched_movies(db, user_id):
    tbl_ratting_movies = db.user_ratting_movies
    watched_movie_df = tbl_ratting_movies[tbl_ratting_movies['user_id'] == user_id]
    watched_movie_df.sort_values(by='timestamp', ascending=False, inplace=True)
    return watched_movie_df

# 过滤出推荐的电影，排除用户看过的电影
def filter_recommended_movies(retrival_movie_ids, watched_movie_ids, movie_id_idx, tbl_movies):
    retrival_set = set(retrival_movie_ids)
    watched_set = set(watched_movie_ids)
    result_set = retrival_set - watched_set
    return tbl_movies[tbl_movies['movie_id'].isin(result_set)].to_json(orient='records')

# 主要路由函数
@app.route('/<user_id>')
def home(user_id):
    user_id = int(user_id)  # 确保 user_id 是整数
    watched_movie_df = get_watched_movies(db, user_id)
    watched_movie_ids = watched_movie_df["movie_id"].values
    lastn_watched_movies = json.loads(watched_movie_df.head(n=30).to_json(orient='records'))
    
    user_emb_query = get_user_emb(user_id_emb_dict, user_id)
    search_idx_result = search_top_n_movies(faiss_index, user_emb_query, TOP_N)
    retrival_movie_ids = [movie_id_idx[idx] for idx in search_idx_result]
    
    result_movies_json_str = filter_recommended_movies(retrival_movie_ids, watched_movie_ids, movie_id_idx, db.movies)
    result_movies = json.loads(result_movies_json_str)

    return render_template('movies.html', watched_movies=lastn_watched_movies, retrival_movies=result_movies)

# 初始化数据库和嵌入向量
db = initialize_database()
item_embs, user_embs, user_id_idx, movie_id_idx = load_embeddings()
user_id_emb_dict = build_user_emb_dict(user_id_idx, user_embs)
faiss_index = initialize_faiss(item_embs, embedding_dim)

if __name__ == '__main__':
    # 运行应用
    app.run(host='0.0.0.0', port=5000, debug=True)