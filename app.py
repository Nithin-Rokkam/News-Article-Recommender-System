from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os
from typing import Optional, List, Dict, Any, Tuple
import re
from datetime import datetime
import logging
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for model and data
data: Optional[pd.DataFrame] = None
tfidv: Optional[TfidfVectorizer] = None
nmf: Optional[NMF] = None
topics: Optional[np.ndarray] = None
cosine_sim: Optional[np.ndarray] = None
indices: Optional[pd.Series] = None

def extract_category(keywords: str) -> str:
    """Extract category from keywords"""
    if pd.isna(keywords):
        return 'General'
    
    keywords_lower = keywords.lower()
    
    # Define category keywords
    categories = {
        'Technology': ['tech', 'software', 'app', 'startup', 'ai', 'machine learning', 'digital', 'innovation'],
        'Business': ['business', 'company', 'market', 'investment', 'finance', 'economy', 'startup'],
        'Politics': ['politics', 'government', 'election', 'policy', 'democrat', 'republican', 'congress'],
        'Health': ['health', 'medical', 'covid', 'vaccine', 'hospital', 'doctor', 'treatment'],
        'Science': ['science', 'research', 'study', 'discovery', 'scientific', 'experiment'],
        'Entertainment': ['movie', 'film', 'celebrity', 'hollywood', 'music', 'entertainment', 'show'],
        'Sports': ['sports', 'football', 'basketball', 'baseball', 'soccer', 'athlete', 'game'],
        'Education': ['education', 'school', 'university', 'student', 'learning', 'academic']
    }
    
    for category, keywords_list in categories.items():
        if any(keyword in keywords_lower for keyword in keywords_list):
            return category
    
    return 'General'

def analyze_sentiment(text: str) -> str:
    """Simple sentiment analysis based on keywords"""
    if pd.isna(text):
        return 'neutral'
    
    text_lower = text.lower()
    
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'positive', 'success', 'win']
    negative_words = ['bad', 'terrible', 'awful', 'negative', 'fail', 'loss', 'problem', 'crisis']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

def estimate_reading_time(text: str) -> int:
    """Estimate reading time in minutes"""
    if pd.isna(text):
        return 1
    
    # Average reading speed: 200 words per minute
    word_count = len(text.split())
    return max(1, round(word_count / 200))

def load_model():
    """Load the trained model and data"""
    global data, tfidv, nmf, topics, cosine_sim, indices
    
    try:
        logger.info("Starting model loading...")
        
        # Check if dataset file exists
        dataset_path = 'Dataset/result_final.csv'
        if not os.path.exists(dataset_path):
            logger.error(f"Dataset file not found at {dataset_path}")
            return False
        
        # Load the dataset
        logger.info("Loading dataset...")
        data = pd.read_csv(dataset_path)
        logger.info(f"Dataset loaded with {len(data)} rows")
        
        # Data cleaning (same as in notebook)
        logger.info("Cleaning data...")
        data.dropna(how='any', subset=['title_summary'], inplace=True)
        data.drop_duplicates(subset=['title'], keep='first', inplace=True)
        data.drop_duplicates(subset=['summary'], keep='first', inplace=True)
        data.drop_duplicates(subset=['text'], keep='first', inplace=True)
        data.drop(labels=['Unnamed: 0', 'Unnamed: 0.1', 'title_summary'], axis=1, inplace=True)
        
        # Add categories based on keywords and content
        logger.info("Adding categories...")
        data['category'] = data['keywords'].apply(extract_category)
        
        # Add sentiment analysis (simple keyword-based)
        logger.info("Adding sentiment analysis...")
        data['sentiment'] = data['text'].apply(analyze_sentiment)
        
        # Add reading time estimation
        logger.info("Adding reading time estimation...")
        data['reading_time'] = data['text'].apply(estimate_reading_time)
        
        # Create soup for TF-IDF
        logger.info("Creating text soup...")
        def create_soup(x):
            return x['title'] + ' ' + x['keywords'] + ' ' + x['summary'] + ' ' + x['text']
        data['soup'] = data.apply(create_soup, axis=1)
        
        # TF-IDF Vectorization
        logger.info("Performing TF-IDF vectorization...")
        tfidv = TfidfVectorizer(strip_accents='ascii', stop_words='english')
        tfidfv_matrix = tfidv.fit_transform(data['soup'])
        
        # NMF for topic modeling
        logger.info("Performing NMF topic modeling...")
        nmf = NMF(n_components=20)
        topics = nmf.fit_transform(tfidfv_matrix)
        
        # Calculate cosine similarity
        logger.info("Calculating cosine similarity...")
        cosine_sim = linear_kernel(topics, topics)
        
        # Create indices mapping
        logger.info("Creating indices mapping...")
        indices = pd.Series(data.index, index=data['title']).drop_duplicates()
        
        logger.info("Model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

# Load model when module is imported (works for both direct run and Gunicorn)
logger.info("Initializing model loading...")
model_loaded = load_model()
if not model_loaded:
    logger.error("Failed to load model during initialization")

def get_recommendations(title: str, num_recommendations: int = 5, category_filter: str = None, 
                       sentiment_filter: str = None, min_similarity: float = 0.0) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Get recommendations for a given article title with filters"""
    if data is None or indices is None or cosine_sim is None:
        return None, "Model not loaded"
    
    if title not in indices:
        return None, "Article not found in dataset"
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Apply similarity threshold
    sim_scores = [score for score in sim_scores if score[1] >= min_similarity]
    
    # Get more candidates for filtering
    candidate_indices = [i[0] for i in sim_scores[1:num_recommendations*3+1]]
    
    # Apply filters
    filtered_indices = []
    for idx in candidate_indices:
        article = data.iloc[idx]
        
        # Category filter
        if category_filter and category_filter != 'All' and article['category'] != category_filter:
            continue
            
        # Sentiment filter
        if sentiment_filter and sentiment_filter != 'All' and article['sentiment'] != sentiment_filter:
            continue
            
        filtered_indices.append(idx)
    
    # Take top recommendations
    final_indices = filtered_indices[:num_recommendations]
    
    recommendations = []
    for i, idx in enumerate(final_indices):
        article = data.iloc[idx]
        sim_score = next(score[1] for score in sim_scores if score[0] == idx)
        
        rec = {
            'rank': i + 1,
            'title': article['title'],
            'summary': article['summary'],
            'link': article['link'],
            'date': str(article['date']) if pd.notna(article['date']) else 'Unknown',
            'similarity_score': round(sim_score, 4),
            'category': article['category'],
            'sentiment': article['sentiment'],
            'reading_time': article['reading_time']
        }
        recommendations.append(rec)
    
    return recommendations, None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/help')
def help_page():
    """Help page"""
    return render_template('help.html')

@app.route('/api/articles')
def get_articles():
    """Get list of all articles for search dropdown"""
    if data is None:
        return jsonify({'articles': []})
    articles = data['title'].tolist()
    return jsonify({'articles': articles})

@app.route('/api/categories')
def get_categories():
    """Get all available categories"""
    if data is None:
        return jsonify({'categories': []})
    
    categories = data['category'].value_counts().to_dict()
    return jsonify({'categories': categories})

@app.route('/api/stats')
def get_stats():
    """Get comprehensive statistics"""
    if data is None:
        return jsonify({'error': 'Data not loaded'})
    
    stats = {
        'total_articles': len(data),
        'categories': data['category'].value_counts().to_dict(),
        'sentiments': data['sentiment'].value_counts().to_dict(),
        'avg_reading_time': round(data['reading_time'].mean(), 1),
        'date_range': {
            'earliest': str(data['date'].min()) if pd.notna(data['date'].min()) else 'Unknown',
            'latest': str(data['date'].max()) if pd.notna(data['date'].max()) else 'Unknown'
        }
    }
    
    return jsonify(stats)

@app.route('/api/recommendations', methods=['POST'])
def api_recommendations():
    """API endpoint to get recommendations with filters"""
    try:
        if data is None or indices is None:
            return jsonify({'error': 'Model not loaded'}), 500
            
        data_req = request.get_json()
        title = data_req.get('title')
        num_recommendations = data_req.get('num_recommendations', 5)
        category_filter = data_req.get('category_filter', 'All')
        sentiment_filter = data_req.get('sentiment_filter', 'All')
        min_similarity = data_req.get('min_similarity', 0.0)
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        recommendations, error = get_recommendations(
            title, num_recommendations, category_filter, sentiment_filter, min_similarity
        )
        
        if error:
            return jsonify({'error': error}), 404
        
        original_article = data.loc[indices[title]]
        
        return jsonify({
            'original_article': {
                'title': title,
                'link': original_article['link'],
                'summary': original_article['summary'],
                'category': original_article['category'],
                'sentiment': original_article['sentiment'],
                'reading_time': original_article['reading_time']
            },
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_articles():
    """Search articles by title with filters"""
    if data is None:
        return jsonify({'articles': []})
        
    query = request.args.get('q', '').lower()
    category = request.args.get('category', 'All')
    sentiment = request.args.get('sentiment', 'All')
    
    if not query:
        return jsonify({'articles': []})
    
    # Filter articles
    matching_articles = data[data['title'].str.lower().str.contains(query, na=False)]
    
    # Apply category filter
    if category != 'All':
        matching_articles = matching_articles[matching_articles['category'] == category]
    
    # Apply sentiment filter
    if sentiment != 'All':
        matching_articles = matching_articles[matching_articles['sentiment'] == sentiment]
    
    results = []
    for _, row in matching_articles.head(10).iterrows():
        results.append({
            'title': row['title'],
            'summary': row['summary'][:200] + '...' if len(row['summary']) > 200 else row['summary'],
            'link': row['link'],
            'category': row['category'],
            'sentiment': row['sentiment'],
            'reading_time': row['reading_time']
        })
    
    return jsonify({'articles': results})

@app.route('/api/trending')
def get_trending():
    """Get trending articles based on similarity scores"""
    if data is None:
        return jsonify({'articles': []})
    
    # Calculate average similarity for each article
    avg_similarities = np.mean(cosine_sim, axis=1)
    data_copy = data.copy()
    data_copy['avg_similarity'] = avg_similarities
    
    # Get top trending articles
    trending = data_copy.nlargest(10, 'avg_similarity')
    
    results = []
    for _, row in trending.iterrows():
        results.append({
            'title': row['title'],
            'summary': row['summary'][:150] + '...' if len(row['summary']) > 150 else row['summary'],
            'link': row['link'],
            'category': row['category'],
            'sentiment': row['sentiment'],
            'reading_time': row['reading_time'],
            'trending_score': round(row['avg_similarity'], 4)
        })
    
    return jsonify({'articles': results})

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    try:
        if data is None or indices is None or cosine_sim is None:
            return jsonify({
                'status': 'unhealthy',
                'message': 'Model not loaded',
                'data_loaded': data is not None,
                'indices_loaded': indices is not None,
                'cosine_sim_loaded': cosine_sim is not None
            }), 503
        
        return jsonify({
            'status': 'healthy',
            'message': 'Model loaded successfully',
            'total_articles': len(data) if data is not None else 0,
            'model_components': {
                'data': data is not None,
                'tfidv': tfidv is not None,
                'nmf': nmf is not None,
                'topics': topics is not None,
                'cosine_sim': cosine_sim is not None,
                'indices': indices is not None
            }
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'message': f'Health check failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000) 