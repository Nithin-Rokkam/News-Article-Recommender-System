import os
import logging
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import linear_kernel
from typing import List, Dict, Any, Optional, Tuple
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
    
    # Simplified categories for memory efficiency
    categories = {
        'Technology': ['tech', 'software', 'ai', 'digital'],
        'Business': ['business', 'company', 'market', 'finance'],
        'Politics': ['politics', 'government', 'election'],
        'Health': ['health', 'medical', 'covid'],
        'General': []  # Default category
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
    
    positive_words = ['good', 'great', 'success', 'win']
    negative_words = ['bad', 'fail', 'loss', 'problem']
    
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
    
    word_count = len(text.split())
    return max(1, round(word_count / 200))

def load_model():
    """Load the trained model and data with memory optimization"""
    global data, tfidv, nmf, topics, cosine_sim, indices
    
    try:
        logger.info("Starting memory-efficient model loading...")
        
        # Check if dataset file exists
        dataset_path = 'Dataset/result_final.csv'
        if not os.path.exists(dataset_path):
            logger.error(f"Dataset file not found at {dataset_path}")
            return False
        
        # Load the dataset
        logger.info("Loading dataset...")
        data = pd.read_csv(dataset_path)
        logger.info(f"Dataset loaded with {len(data)} rows")
        
        # Use only a subset for memory efficiency (first 1000 articles)
        if len(data) > 1000:
            logger.info("Using subset of 1000 articles for memory efficiency")
            data = data.head(1000).copy()
        
        # Basic data cleaning
        logger.info("Cleaning data...")
        data.dropna(how='any', subset=['title_summary'], inplace=True)
        data.drop_duplicates(subset=['title'], keep='first', inplace=True)
        data.drop(labels=['Unnamed: 0', 'Unnamed: 0.1', 'title_summary'], axis=1, inplace=True, errors='ignore')
        
        # Add simplified categories
        logger.info("Adding categories...")
        data['category'] = data['keywords'].apply(extract_category)
        
        # Add sentiment analysis
        logger.info("Adding sentiment analysis...")
        data['sentiment'] = data['text'].apply(analyze_sentiment)
        
        # Add reading time estimation
        logger.info("Adding reading time estimation...")
        data['reading_time'] = data['text'].apply(estimate_reading_time)
        
        # Create simplified soup for TF-IDF
        logger.info("Creating text soup...")
        def create_soup(x):
            return x['title'] + ' ' + x['summary'][:500]  # Limit summary length
        data['soup'] = data.apply(create_soup, axis=1)
        
        # Memory-efficient TF-IDF Vectorization
        logger.info("Performing TF-IDF vectorization...")
        tfidv = TfidfVectorizer(
            strip_accents='ascii', 
            stop_words='english',
            max_features=2000,  # Very limited features
            min_df=3,           # Higher minimum frequency
            max_df=0.9          # Lower maximum frequency
        )
        tfidfv_matrix = tfidv.fit_transform(data['soup'])
        
        # Memory-efficient NMF
        logger.info("Performing NMF topic modeling...")
        nmf = NMF(n_components=5, random_state=42)  # Very few components
        topics = nmf.fit_transform(tfidfv_matrix)
        
        # Calculate cosine similarity
        logger.info("Calculating cosine similarity...")
        cosine_sim = linear_kernel(topics, topics)
        
        # Create indices mapping
        logger.info("Creating indices mapping...")
        indices = pd.Series(data.index, index=data['title']).drop_duplicates()
        
        logger.info("Memory-efficient model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

# Load model when module is imported
logger.info("Initializing memory-efficient model loading...")
model_loaded = load_model()
if not model_loaded:
    logger.error("Failed to load model during initialization")

def get_recommendations(title: str, num_recommendations: int = 5) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Get recommendations for a given article title"""
    if data is None or indices is None or cosine_sim is None:
        return None, "Model not loaded"
    
    if title not in indices:
        return None, "Article not found in dataset"
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top recommendations
    top_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
    
    recommendations = []
    for i, idx in enumerate(top_indices):
        article = data.iloc[idx]
        sim_score = next(score[1] for score in sim_scores if score[0] == idx)
        
        rec = {
            'rank': i + 1,
            'title': article['title'],
            'summary': article['summary'][:200] + '...' if len(article['summary']) > 200 else article['summary'],
            'link': article['link'],
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

@app.route('/health')
def health_check():
    """Health check endpoint"""
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
            'message': 'Memory-efficient model loaded successfully',
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

@app.route('/api/articles')
def get_articles():
    """Get list of all articles for search dropdown"""
    if data is None:
        return jsonify({'articles': []})
    articles = data['title'].tolist()
    return jsonify({'articles': articles})

@app.route('/api/recommendations', methods=['POST'])
def api_recommendations():
    """API endpoint to get recommendations"""
    try:
        if data is None or indices is None:
            return jsonify({'error': 'Model not loaded'}), 500
            
        data_req = request.get_json()
        title = data_req.get('title')
        num_recommendations = data_req.get('num_recommendations', 5)
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        recommendations, error = get_recommendations(title, num_recommendations)
        
        if error:
            return jsonify({'error': error}), 404
        
        original_article = data.loc[indices[title]]
        
        return jsonify({
            'original_article': {
                'title': title,
                'link': original_article['link'],
                'summary': original_article['summary'][:200] + '...' if len(original_article['summary']) > 200 else original_article['summary'],
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
    """Search articles by title"""
    if data is None:
        return jsonify({'articles': []})
        
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'articles': []})
    
    # Filter articles
    matching_articles = data[data['title'].str.lower().str.contains(query, na=False)]
    
    results = []
    for _, row in matching_articles.head(10).iterrows():
        results.append({
            'title': row['title'],
            'summary': row['summary'][:150] + '...' if len(row['summary']) > 150 else row['summary'],
            'link': row['link'],
            'category': row['category'],
            'sentiment': row['sentiment'],
            'reading_time': row['reading_time']
        })
    
    return jsonify({'articles': results})

if __name__ == '__main__':
    print("Starting memory-efficient Flask app...")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 