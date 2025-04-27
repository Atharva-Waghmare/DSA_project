import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.linalg import svd
import os
import warnings
warnings.filterwarnings('ignore')

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mood-to-Genre Mapping
mood_to_genres = {
    'light': [
        'Humor', 'Comedy', 'Romance', 'Contemporary Romance', 'Chick Lit',
        'Childrens', 'Picture Books'
    ],
    'thought-provoking': [
        'Philosophy', 'Literary Fiction', 'Psychology', 'Sociology', 'Classics',
        'Criticism', 'Literary Criticism'
    ],
    'escape': [
        'Fantasy', 'Science Fiction', 'Science Fiction Fantasy', 'Adventure',
        'Epic Fantasy', 'Urban Fantasy', 'Paranormal', 'Space Opera', 'Dystopia'
    ],
    'learn': [
        'Nonfiction', 'Biography', 'Autobiography', 'Memoir', 'Biography Memoir',
        'History', 'Science', 'Popular Science', 'Reference', 'Education'
    ],
    'emotional': [
        'Drama', 'Family', 'Womens Fiction', 'Literary Fiction', 'Romance',
        'Inspirational', 'Young Adult'
    ],
    'adventurous': [
        'Adventure', 'Action', 'Thriller', 'Mystery Thriller', 'Spy Thriller',
        'Historical Fiction', 'War', 'Military Fiction'
    ]
}

# Era-to-Genre Proxy Mapping
era_to_genres = {
    'classic': ['Classics', '19th Century', 'Ancient', 'Ancient History'],
    'mid-century': ['20th Century'],
    'modern': ['20th Century', '21st Century'],
    'contemporary': ['21st Century', 'Contemporary'],
    'any': None  # No filter
}

# Map frontend genre values to actual genres
genre_mapping = {
    'fiction': 'Fiction',
    'fantasy': 'Fantasy',
    'scifi': 'Science Fiction',
    'mystery': 'Mystery',
    'romance': 'Romance',
    'historical': 'Historical Fiction',
    'biography': 'Biography',
    'nonfiction': 'Nonfiction'
}

# Load the dataset
@app.on_event("startup")
async def startup_db_client():
    try:
        # Check if the processed file exists, if not, process it
        base_path = os.path.join(os.path.dirname(__file__), '')
        processed_path = os.path.join(base_path, 'book_processed.csv')
        
        if os.path.exists(processed_path):
            app.book_df = pd.read_csv(processed_path)
        else:
            # If the processed file doesn't exist, read raw data and process it
            raw_path = os.path.join(base_path, 'book_processed.csv')
            if not os.path.exists(raw_path):
                raise FileNotFoundError(f"Dataset not found at {raw_path}")
                
            book_df = pd.read_csv(raw_path, low_memory=False)
            
            # Preprocessing
            book_df = book_df.rename(columns={
                'rating': 'avg_rating',
                'totalratings': 'num_votes'
            })
            book_df['item_id'] = book_df['isbn']
            book_df = book_df.dropna(subset=['item_id', 'title'])
            book_df['genres'] = book_df.get('genre', 'Unknown').fillna('Unknown')
            book_df['img'] = book_df['img'].fillna('Unknown')
            book_df = book_df.drop_duplicates(subset=['item_id'])
            book_df['domain'] = 'book'
            book_df = book_df[['item_id', 'title', 'author', 'genres', 'avg_rating', 'num_votes', 'domain', 'img']]
            
            # Save the processed dataset
            os.makedirs(base_path, exist_ok=True)
            book_df.to_csv(processed_path, index=False)
            app.book_df = book_df
            
        print(f"Loaded book dataset with {len(app.book_df)} records")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        # Provide a small sample dataset for testing if real data can't be loaded
        app.book_df = pd.DataFrame({
            'item_id': ['1', '2', '3', '4', '5'],
            'title': ['To Kill a Mockingbird', '1984', 'The Great Gatsby', 'Pride and Prejudice', 'The Catcher in the Rye'],
            'author': ['Harper Lee', 'George Orwell', 'F. Scott Fitzgerald', 'Jane Austen', 'J.D. Salinger'],
            'genres': ['Fiction,Classics', 'Fiction,Science Fiction,Classics', 'Fiction,Classics', 'Fiction,Classics,Romance', 'Fiction,Classics'],
            'avg_rating': [4.3, 4.2, 3.9, 4.3, 3.8],
            'num_votes': [4000, 3500, 3200, 2800, 2500],
            'domain': ['book', 'book', 'book', 'book', 'book'],
            'img': ['https://images-na.ssl-images-amazon.com/images/I/81f7o6uZjFL.jpg', 
                    'https://images-na.ssl-images-amazon.com/images/I/71kxa1-0mfL.jpg',
                    'https://images-na.ssl-images-amazon.com/images/I/71FTb9X6wsL.jpg', 
                    'https://images-na.ssl-images-amazon.com/images/I/71Q1tPupKjL.jpg', 
                    'https://images-na.ssl-images-amazon.com/images/I/91HPG31dTwL.jpg']
        })


class RecommendationRequest(BaseModel):
    book_titles: list
    mood: str = None
    era: str = None  
    genre: str = None

# Function to Filter Dataset Based on Mood, Era, and Genre
def filter_dataset(book_df, mood, era, genre):
    """Filter the dataset based on user-selected mood, era, and genre."""
    filtered_df = book_df.copy()
    
    # Step 1: Genre Filtering
    target_genres = []
    if genre and genre in genre_mapping:
        target_genres.append(genre_mapping[genre])
    
    if mood and mood in mood_to_genres:
        target_genres.extend(mood_to_genres[mood])
    
    target_genres = list(set(target_genres))  # Remove duplicates
    
    if target_genres:
        genre_filter = filtered_df['genres'].apply(
            lambda x: any(g in str(x).split(',') for g in target_genres)
        )
        filtered_df = filtered_df[genre_filter]
    
    # Step 2: Era Filtering
    if era and era in era_to_genres and era_to_genres[era]:
        era_genres = era_to_genres[era]
        era_filter = filtered_df['genres'].apply(
            lambda x: any(g in str(x).split(',') for g in era_genres)
        )
        filtered_df = filtered_df[era_filter]
    
    if len(filtered_df) < 1:  # Fallback if too few books match
        print("Warning: Too few books match filters. Using broader dataset.")
        return book_df
    
    return filtered_df

# Function to Build Feature Matrix and Train Model
def build_model(filtered_df):
    """Build the feature matrix and train the SVD-KNN model on the filtered dataset."""
    # Feature Engineering
    tfidf = TfidfVectorizer(tokenizer=lambda x: str(x).split(','), lowercase=True, token_pattern=None)
    genre_features = tfidf.fit_transform(filtered_df['genres'].fillna('Unknown'))
    
    scaler = StandardScaler()
    numerical_features = scaler.fit_transform(filtered_df[['avg_rating', 'num_votes']].fillna(0))
    
    feature_matrix = np.hstack((genre_features.toarray(), numerical_features))
    
    # Apply SVD
    U, Sigma, Vt = svd(feature_matrix, full_matrices=False)
    k = min(50, feature_matrix.shape[1] - 1)  # Adjust k if feature matrix is smaller
    U_k = U[:, :k]
    Sigma_k = np.diag(Sigma[:k])
    book_latent_matrix = np.dot(U_k, Sigma_k)
    
    # Apply KNN
    knn = NearestNeighbors(n_neighbors=6, metric='cosine')
    knn.fit(book_latent_matrix)
    
    return book_latent_matrix, knn, filtered_df

# Function to Find Similar Books
def find_similar_books(book_titles, book_df, filtered_df, book_latent_matrix, knn_model, n_recommendations=5):
    """Find similar books based on input book titles."""
    # Find matching books in the filtered dataset
    book_indices = []
    
    for title in book_titles:
        title = title.lower().strip()
        matching_books = filtered_df[filtered_df['title'].str.lower().str.contains(title, na=False)]
        if not matching_books.empty:
            book_indices.append(filtered_df.index.get_loc(matching_books.index[0]))
    
    if not book_indices:
        # Fallback to popular books if no matches
        return book_df.sort_values('num_votes', ascending=False).head(n_recommendations)
    
    # Aggregate latent features of input books
    aggregated_features = np.mean(book_latent_matrix[book_indices], axis=0).reshape(1, -1)
    
    # Find nearest neighbors
    distances, indices = knn_model.kneighbors(aggregated_features, n_neighbors=n_recommendations + len(book_indices))
    
    # Filter out input books from recommendations
    input_indices_set = set(book_indices)
    similar_indices = [idx for idx in indices[0] if idx not in input_indices_set][:n_recommendations]
    
    # Map indices back to the filtered DataFrame
    similar_books = filtered_df.iloc[similar_indices][['title', 'author', 'genres', 'avg_rating', 'num_votes', 'img']]
    
    return similar_books

@app.get("/")
def read_root():
    return {"message": "Book Recommendation API is running"}

@app.post("/recommendations/")
async def get_recommendations(request: RecommendationRequest):
    try:
        # Check if we have book titles
        if not request.book_titles or len(request.book_titles) == 0:
            raise HTTPException(status_code=400, detail="No book titles provided")
            
        # Filter the dataset based on user preferences
        filtered_df = filter_dataset(app.book_df, request.mood, request.era, request.genre)
        
        # Build the model
        book_latent_matrix, knn, filtered_df = build_model(filtered_df)
        
        # Get recommendations
        similar_books = find_similar_books(
            request.book_titles, 
            app.book_df,
            filtered_df, 
            book_latent_matrix, 
            knn, 
            n_recommendations=5
        )
        
        # Convert results to a list of dictionaries
        recommendations = []
        for _, book in similar_books.iterrows():
            try:
                year = int(book.get('year', 0)) if 'year' in book else None
                
                # Ensure the image URL is valid
                img_url = book.get('img', '')
                if img_url == 'Unknown' or not img_url:
                    img_url = "https://via.placeholder.com/150x225?text=No+Cover"
                    
                recommendations.append({
                    'id': book.get('item_id', ''),
                    'title': book.get('title', 'Unknown Title'),
                    'author': book.get('author', 'Unknown Author'),
                    'year': year,
                    'rating': float(book.get('avg_rating', 0)),
                    'image': img_url
                })
            except Exception as e:
                print(f"Error processing book: {e}")
                continue
        
        return {"recommendations": recommendations}
    
    except Exception as e:
        print(f"Error in recommendation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)