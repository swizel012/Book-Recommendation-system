from flask import Flask, render_template, request
import pandas as pd
import ast

app = Flask(__name__)

# Load and clean dataset
df = pd.read_csv('C://Users//91749//Downloads//Book-Recommendation-System-main/Book-Recommendation-System-main/goodreads_data.csv')
df['Genres'] = df['Genres'].apply(lambda x: ast.literal_eval(x))  # Convert string to list
df['Avg_Rating'] = pd.to_numeric(df['Avg_Rating'], errors='coerce')
df['Num_Ratings'] = pd.to_numeric(df['Num_Ratings'].str.replace(',', ''), errors='coerce')

# Get unique genre list
all_genres = sorted({genre for genres in df['Genres'] for genre in genres})

# Recommendation function
'''
def recommend_by_genre(selected_genre):
    genre_books = df[df['Genres'].apply(lambda genres: selected_genre in genres)]
    top_books = genre_books.sort_values(by='Avg_Rating', ascending=False)[['Book', 'Author']].drop_duplicates()
    return top_books.head(10)

def recommend_by_genre(selected_genre):
    genre_books = df[df['Genres'].apply(lambda genres: selected_genre in genres)]
    
    # Sort by Avg_Rating and Num_Ratings (both descending)
    top_books = genre_books.sort_values(
        by=['Avg_Rating', 'Num_Ratings'], 
        ascending=[False, False]
    )[['Book', 'Author', 'Avg_Rating', 'Num_Ratings']].drop_duplicates()

    return top_books.head(10)
'''
def recommend_by_genre(selected_genre):
    genre_books = df[df['Genres'].apply(lambda genres: selected_genre in genres)].copy()

    # Ensure Num_Ratings is float
    genre_books['Num_Ratings'] = genre_books['Num_Ratings'].astype(float)

    # Calculate C (mean average rating across the genre)
    C = genre_books['Avg_Rating'].mean()

    # Calculate m (minimum votes required to be listed)
    m = genre_books['Num_Ratings'].quantile(0.80)  # Top 20% books by number of ratings

    # Filter books that have enough votes
    qualified = genre_books[genre_books['Num_Ratings'] >= m].copy()

    # Compute rank-aware weighted score
    def weighted_score(x):
        v = x['Num_Ratings']
        R = x['Avg_Rating']
        return (v / (v + m)) * R + (m / (v + m)) * C

    qualified['Score'] = qualified.apply(weighted_score, axis=1)

    # Sort by the computed score
    top_books = qualified.sort_values(by='Score', ascending=False)[['Book', 'Author', 'Avg_Rating', 'Num_Ratings', 'Score']].drop_duplicates()

    return top_books.head(10)


@app.route('/')
def index():
    return render_template('index.html', genres=all_genres)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_genre = request.form['genre']
    recommendations = recommend_by_genre(selected_genre)
    return render_template('recommendations.html', books=recommendations, genre=selected_genre)

if __name__ == '__main__':
    app.run(debug=True)
