import pandas as pd
import numpy as np

# 使用pandas模拟数据库服务
class MemDatabase:
    def __init__(self, data_path="./"):
        self.data_path = data_path
        self.user_cols = ['user_id', 'gender', 'age', 'occupation', 'zip']
        self.rating_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
        self.movie_cols = ['movie_id', 'title', 'genres']

    def load_users(self):
        """加载用户数据"""
        user_file = f"{self.data_path}/users.dat"
        return pd.read_csv(user_file, sep='::', header=None, names=self.user_cols, engine='python')

    def load_ratings(self):
        """加载评分数据"""
        ratings_file = f"{self.data_path}/ratings.dat"
        return pd.read_csv(ratings_file, sep='::', header=None, names=self.rating_cols, engine='python')

    def load_movies(self):
        """加载电影数据，并处理电影类型"""
        movies_file = f"{self.data_path}/movies.dat"
        movies = pd.read_csv(movies_file, sep='::', header=None, names=self.movie_cols, encoding="unicode_escape", engine='python')
        movies['genres'] = movies['genres'].map(lambda x: x.split('|')[0])
        return movies

    def load_data(self):
        """加载并合并所有数据"""
        self.users = self.load_users()
        self.ratings = self.load_ratings()
        self.movies = self.load_movies()
        self.user_ratting_movies = pd.merge(self.ratings, self.movies, on='movie_id')
        
