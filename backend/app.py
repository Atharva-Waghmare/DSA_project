from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse, mae
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Mood-to-genre mapping
mood_to_genre = {
    'Happy': 'Comedy',
    'Sad': 'Drama',
    'Excited': 'Action',
    'Relaxed': 'Romance',
    'Curious': 'Mystery'
}

# Load movie and TV show dataset
movie_path = 'data/merged_movie_data.csv'  # Path relative to backend folder
try:
    full_df = pd.read_csv(movie_path, low_memory=False)
    full_df = full_df[['movie_id', 'title', 'genre', 'year', 'avg_rating', 'type']].dropna(subset=['movie_id', 'avg_rating'])
    
    # Split into movies and TV shows
    movie_df = full_df[full_df['type'] == 'movie'].sort_values('avg_rating', ascending=False).head(10000)
    tvshow_df = full_df[full_df['type'] == 'tv_show'].sort_values('avg_rating', ascending=False).head(10000)
    
    print("Sampled movie dataset shape:", movie_df.shape)
    print("Sampled TV show dataset shape:", tvshow_df.shape)
except FileNotFoundError:
    print(f"Error: File not found at {movie_path}. Please place it in the 'data' folder.")
    raise

# Synthetic interactions for movies
np.random.seed(42)
num_users = 1000
num_movies = len(movie_df)
movie_interactions = []
for user_id in range(1, num_users + 1):
    num_ratings = np.random.randint(int(0.1 * num_movies), int(0.3 * num_movies))
    movie_indices = np.random.choice(num_movies, num_ratings, replace=False)
    for idx in movie_indices:
        movie_id = movie_df.iloc[idx]['movie_id']
        rating = np.clip(np.random.normal(3.9, 0.3), 1, 5)
        movie_interactions.append({'user_id': f'user{user_id}', 'movie_id': movie_id, 'rating': rating})
movie_interactions_df = pd.DataFrame(movie_interactions)
print("Synthetic movie interactions shape:", movie_interactions_df.shape)

# Movie model
movie_reader = Reader(rating_scale=(1, 5))
movie_data = Dataset.load_from_df(movie_interactions_df[['user_id', 'movie_id', 'rating']], movie_reader)
movie_trainset, movie_testset = train_test_split(movie_data, test_size=0.2, random_state=42)
movie_svd = SVD(n_factors=150, n_epochs=50, lr_all=0.001, reg_all=0.1, random_state=42)
movie_svd.fit(movie_trainset)
print("SVD model for movies trained successfully.")
movie_predictions = movie_svd.test(movie_testset)
movie_rmse = rmse(movie_predictions, verbose=True)
movie_mae = mae(movie_predictions, verbose=True)
movie_precision_5 = precision_at_k(movie_predictions, k=5, threshold=3.5)
print(f"Movie Precision@5: {movie_precision_5:.4f}")
print("\nEvaluation Metrics Summary (Movies):")
print(f"RMSE: {movie_rmse:.4f}")
print(f"MAE: {movie_mae:.4f}")
print(f"Precision@5: {movie_precision_5:.4f}")

# Synthetic interactions for TV shows
num_tvshows = len(tvshow_df)
tvshow_interactions = []
for user_id in range(1, num_users + 1):
    num_ratings = np.random.randint(int(0.1 * num_tvshows), int(0.3 * num_tvshows))
    tvshow_indices = np.random.choice(num_tvshows, num_ratings, replace=False)
    for idx in tvshow_indices:
        movie_id = tvshow_df.iloc[idx]['movie_id']
        rating = np.clip(np.random.normal(3.9, 0.3), 1, 5)
        tvshow_interactions.append({'user_id': f'user{user_id}', 'movie_id': movie_id, 'rating': rating})
tvshow_interactions_df = pd.DataFrame(tvshow_interactions)
print("Synthetic TV show interactions shape:", tvshow_interactions_df.shape)

# TV show model
tvshow_reader = Reader(rating_scale=(1, 5))
tvshow_data = Dataset.load_from_df(tvshow_interactions_df[['user_id', 'movie_id', 'rating']], tvshow_reader)
tvshow_trainset, tvshow_testset = train_test_split(tvshow_data, test_size=0.2, random_state=42)
tvshow_svd = SVD(n_factors=150, n_epochs=50, lr_all=0.001, reg_all=0.1, random_state=42)
tvshow_svd.fit(tvshow_trainset)
print("SVD model for TV shows trained successfully.")
tvshow_predictions = tvshow_svd.test(tvshow_testset)
tvshow_rmse = rmse(tvshow_predictions, verbose=True)
tvshow_mae = mae(tvshow_predictions, verbose=True)
tvshow_precision_5 = precision_at_k(tvshow_predictions, k=5, threshold=3.5)
print(f"TV Show Precision@5: {tvshow_precision_5:.4f}")
print("\nEvaluation Metrics Summary (TV Shows):")
print(f"RMSE: {tvshow_rmse:.4f}")
print(f"MAE: {tvshow_mae:.4f}")
print(f"Precision@5: {tvshow_precision_5:.4f}")

# Load anime dataset
anime_path = 'data/anime_processed.csv'  # Path relative to backend folder
ratings_path = 'data/ratings_processed_sample.csv'  # Path relative to backend folder
try:
    anime_df = pd.read_csv(anime_path)
    anime_ratings_df = pd.read_csv(ratings_path)
    print("Anime dataset shape:", anime_df.shape)
    print("Anime ratings dataset shape:", anime_ratings_df.shape)
except FileNotFoundError:
    print(f"Error: Anime files not found at {anime_path} or {ratings_path}. Please place them in the 'data' folder.")
    raise

# Anime model
anime_reader = Reader(rating_scale=(1, 10))
anime_data = Dataset.load_from_df(anime_ratings_df[['user_id', 'anime_id', 'user_rating']], anime_reader)
anime_trainset, anime_testset = train_test_split(anime_data, test_size=0.2, random_state=42)
anime_svd = SVD(n_factors=150, n_epochs=50, lr_all=0.001, reg_all=0.1, random_state=42)
anime_svd.fit(anime_trainset)
print("SVD model for anime trained successfully.")
anime_predictions = anime_svd.test(anime_testset)
anime_rmse = rmse(anime_predictions, verbose=True)
anime_mae = mae(anime_predictions, verbose=True)
anime_precision_5 = precision_at_k(anime_predictions, k=5, threshold=7.0)
print(f"Anime Precision@5: {anime_precision_5:.4f}")
print("\nEvaluation Metrics Summary (Anime):")
print(f"RMSE: {anime_rmse:.4f}")
print(f"MAE: {anime_mae:.4f}")
print(f"Precision@5: {anime_precision_5:.4f}")

# Load book dataset
book_path = 'data/book_processed.csv'  # Path relative to backend folder
try:
    book_df = pd.read_csv(book_path, low_memory=False)
    book_df = book_df[['item_id', 'title', 'author', 'genres', 'avg_rating']].dropna(subset=['item_id', 'avg_rating'])
    book_df = book_df.sort_values('avg_rating', ascending=False).head(10000)
    print("Loaded book dataset shape:", book_df.shape)
except FileNotFoundError:
    print(f"Error: Book file not found at {book_path}. Please place it in the 'data' folder.")
    raise

# Synthetic interactions for books
num_books = len(book_df)
book_interactions = []
for user_id in range(1, num_users + 1):
    num_ratings = np.random.randint(int(0.1 * num_books), int(0.3 * num_books))
    book_indices = np.random.choice(num_books, num_ratings, replace=False)
    for idx in book_indices:
        item_id = book_df.iloc[idx]['item_id']
        rating = np.clip(np.random.normal(3.9, 0.3), 1, 5)
        book_interactions.append({'user_id': f'user{user_id}', 'item_id': item_id, 'rating': rating})
book_interactions_df = pd.DataFrame(book_interactions)
print("Synthetic book interactions shape:", book_interactions_df.shape)

# Book model
book_reader = Reader(rating_scale=(1, 5))
book_data = Dataset.load_from_df(book_interactions_df[['user_id', 'item_id', 'rating']], book_reader)
book_trainset, book_testset = train_test_split(book_data, test_size=0.2, random_state=42)
book_svd = SVD(n_factors=150, n_epochs=50, lr_all=0.001, reg_all=0.1, random_state=42)
book_svd.fit(book_trainset)
print("SVD model for books trained successfully.")
book_predictions = book_svd.test(book_testset)
book_rmse = rmse(book_predictions, verbose=True)
book_mae = mae(book_predictions, verbose=True)
book_precision_5 = precision_at_k(book_predictions, k=5, threshold=3.5)
print(f"Book Precision@5: {book_precision_5:.4f}")
print("\nEvaluation Metrics Summary (Books):")
print(f"RMSE: {book_rmse:.4f}")
print(f"MAE: {book_mae:.4f}")
print(f"Precision@5: {book_precision_5:.4f}")

def precision_at_k(predictions, k=5, threshold=3.5):
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    precisions = {}
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        top_k = user_ratings[:k]
        relevant = sum(1 for est, true_r in top_k if true_r >= threshold)
        precisions[uid] = relevant / k if k > 0 else 0
    return sum(prec for prec in precisions.values()) / len(precisions) if precisions else 0

# Unified Search Endpoint
@app.route('/search', methods=['GET'])
def search():
    type_param = request.args.get('type', '').lower()
    query = request.args.get('query', '').lower()
    
    if not query:
        return jsonify([])
    
    if type_param == 'movies':
        matches = movie_df[movie_df['title'].str.lower().str.contains(query, na=False)]
        results = matches[['movie_id', 'title', 'year']].head(10).to_dict(orient='records')
    elif type_param == 'tvshows':
        matches = tvshow_df[tvshow_df['title'].str.lower().str.contains(query, na=False)]
        results = matches[['movie_id', 'title', 'year']].head(10).to_dict(orient='records')
    elif type_param == 'anime':
        matches = anime_df[anime_df['title'].str.lower().str.contains(query, na=False)]
        results = matches[['anime_id', 'title', 'year']].head(10).to_dict(orient='records')
    elif type_param == 'books':
        matches = book_df[book_df['title'].str.lower().str.contains(query, na=False)]
        results = matches[['item_id', 'title', 'author']].head(10).to_dict(orient='records')
    else:
        return jsonify({"error": "Invalid type. Use 'movies', 'tvshows', 'anime', or 'books'."}), 400
    
    return jsonify(results)

# Unified Recommend Endpoint
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    type_param = data.get('type', '').lower()
    favorites = data.get('favorites', [])
    preferences = data.get('preferences', {})

    if not favorites:
        return jsonify({"error": "Please provide at least one favorite."}), 400
    if len(favorites) > 5:
        return jsonify({"error": "Maximum of 5 favorites allowed."}), 400

    new_user_id = 'new_user'
    
    if type_param == 'movies':
        global movie_interactions_df
        new_interactions = [{'user_id': new_user_id, 'movie_id': movie_id, 'rating': 4.5} for movie_id in favorites]
        movie_interactions_df = pd.concat([movie_interactions_df, pd.DataFrame(new_interactions)], ignore_index=True)
        
        rated_items = set(favorites)
        all_items = set(movie_df['movie_id'])
        unrated_items = list(all_items - rated_items)
        
        predictions = []
        for item_id in unrated_items:
            pred = movie_svd.predict(new_user_id, item_id)
            predictions.append({'movie_id': item_id, 'predicted_rating': pred.est})
        
        predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
        top_predictions = predictions[:10]
        recommendations_df = pd.DataFrame(top_predictions)
        recommendations_df = recommendations_df.merge(movie_df, on='movie_id', how='left')
        
        item_id_col = 'movie_id'
        df = movie_df
        svd_model = movie_svd
    elif type_param == 'tvshows':
        global tvshow_interactions_df
        new_interactions = [{'user_id': new_user_id, 'movie_id': movie_id, 'rating': 4.5} for movie_id in favorites]
        tvshow_interactions_df = pd.concat([tvshow_interactions_df, pd.DataFrame(new_interactions)], ignore_index=True)
        
        rated_items = set(favorites)
        all_items = set(tvshow_df['movie_id'])
        unrated_items = list(all_items - rated_items)
        
        predictions = []
        for item_id in unrated_items:
            pred = tvshow_svd.predict(new_user_id, item_id)
            predictions.append({'movie_id': item_id, 'predicted_rating': pred.est})
        
        predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
        top_predictions = predictions[:10]
        recommendations_df = pd.DataFrame(top_predictions)
        recommendations_df = recommendations_df.merge(tvshow_df, on='movie_id', how='left')
        
        item_id_col = 'movie_id'
        df = tvshow_df
        svd_model = tvshow_svd
    elif type_param == 'anime':
        global anime_ratings_df
        new_interactions = [{'user_id': new_user_id, 'anime_id': anime_id, 'user_rating': 8.0} for anime_id in favorites]
        anime_ratings_df = pd.concat([anime_ratings_df, pd.DataFrame(new_interactions)], ignore_index=True)
        
        rated_items = set(favorites)
        all_items = set(anime_df['anime_id'])
        unrated_items = list(all_items - rated_items)
        
        predictions = []
        for item_id in unrated_items:
            pred = anime_svd.predict(new_user_id, item_id)
            predictions.append({'anime_id': item_id, 'predicted_rating': pred.est})
        
        predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
        top_predictions = predictions[:10]
        recommendations_df = pd.DataFrame(top_predictions)
        recommendations_df = recommendations_df.merge(anime_df, on='anime_id', how='left')
        
        item_id_col = 'anime_id'
        df = anime_df
        svd_model = anime_svd
    elif type_param == 'books':
        global book_interactions_df
        new_interactions = [{'user_id': new_user_id, 'item_id': item_id, 'rating': 4.5} for item_id in favorites]
        book_interactions_df = pd.concat([book_interactions_df, pd.DataFrame(new_interactions)], ignore_index=True)
        
        rated_items = set(favorites)
        all_items = set(book_df['item_id'])
        unrated_items = list(all_items - rated_items)
        
        predictions = []
        for item_id in unrated_items:
            pred = book_svd.predict(new_user_id, item_id)
            predictions.append({'item_id': item_id, 'predicted_rating': pred.est})
        
        predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
        top_predictions = predictions[:10]
        recommendations_df = pd.DataFrame(top_predictions)
        recommendations_df = recommendations_df.merge(book_df, on='item_id', how='left')
        
        item_id_col = 'item_id'
        df = book_df
        svd_model = book_svd
    else:
        return jsonify({"error": "Invalid type. Use 'movies', 'tvshows', 'anime', or 'books'."}), 400

    genre = preferences.get('genre')
    mood = preferences.get('mood')
    era = preferences.get('era')

    genre_filters = []
    if genre and genre != 'Select a genre':
        genre_filters.append(genre)
    if mood and mood in mood_to_genre:
        genre_filters.append(mood_to_genre[mood])

    if genre_filters:
        combined_filter = '|'.join(genre_filters)
        recommendations_df = recommendations_df[recommendations_df['genre'].str.contains(combined_filter, na=False)]

    if era and era != 'Select an era':
        if era == '1900-1950':
            recommendations_df = recommendations_df[(recommendations_df['year'] >= 1900) & (recommendations_df['year'] <= 1950)]
        elif era == '1951-2000':
            recommendations_df = recommendations_df[(recommendations_df['year'] >= 1951) & (recommendations_df['year'] <= 2000)]
        elif era == '2001-2025':
            recommendations_df = recommendations_df[(recommendations_df['year'] >= 2001) & (recommendations_df['year'] <= 2025)]

    if recommendations_df.empty:
        recommendations_df = pd.DataFrame(top_predictions[:5]).merge(df, on=item_id_col, how='left')

    recommendations = recommendations_df.head(5)[['title', 'year', 'predicted_rating']].to_dict(orient='records')
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 