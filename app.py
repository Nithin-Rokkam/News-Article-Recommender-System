from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os
from typing import Optional, List, Dict, Any, Tuple

app = Flask(__name__)

# Global variables to store the model and data
data: Optional[pd.DataFrame] = None
tfidv: Optional[TfidfVectorizer] = None
nmf: Optional[NMF] = None
topics: Optional[np.ndarray] = None
cosine_sim: Optional[np.ndarray] = None
indices: Optional[pd.Series] = None

def load_model():
    """Load the trained model and data"""
    global data, tfidv, nmf, topics, cosine_sim, indices
    
    # Load the dataset
    data = pd.read_csv('Dataset/result_final.csv')
    
    # Data cleaning (same as in notebook)
    data.dropna(how='any', subset=['title_summary'], inplace=True)
    data.drop_duplicates(subset=['title'], keep='first', inplace=True)
    data.drop_duplicates(subset=['summary'], keep='first', inplace=True)
    data.drop_duplicates(subset=['text'], keep='first', inplace=True)
    data.drop(labels=['Unnamed: 0', 'Unnamed: 0.1', 'title_summary'], axis=1, inplace=True)
    
    # Create soup for TF-IDF
    def create_soup(x):
        return x['title'] + ' ' + x['keywords'] + ' ' + x['summary'] + ' ' + x['text']
    data['soup'] = data.apply(create_soup, axis=1)
    
    # TF-IDF Vectorization
    tfidv = TfidfVectorizer(strip_accents='ascii', stop_words='english')
    tfidfv_matrix = tfidv.fit_transform(data['soup'])
    
    # NMF for topic modeling
    nmf = NMF(n_components=20)
    topics = nmf.fit_transform(tfidfv_matrix)
    
    # Calculate cosine similarity
    cosine_sim = linear_kernel(topics, topics)
    
    # Create indices mapping
    indices = pd.Series(data.index, index=data['title']).drop_duplicates()
    
    print("Model loaded successfully!")

def get_recommendations(title: str, num_recommendations: int = 5) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Get recommendations for a given article title"""
    if data is None or indices is None or cosine_sim is None:
        return None, "Model not loaded"
    
    if title not in indices:
        return None, "Article not found in dataset"
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    
    news_indices = [i[0] for i in sim_scores]
    
    recommendations = []
    for i, idx in enumerate(news_indices):
        rec = {
            'rank': i + 1,
            'title': data['title'].iloc[idx],
            'summary': data['summary'].iloc[idx],
            'link': data['link'].iloc[idx],
            'date': str(data['date'].iloc[idx]) if pd.notna(data['date'].iloc[idx]) else 'Unknown',
            'similarity_score': round(sim_scores[i][1], 4)
        }
        recommendations.append(rec)
    
    return recommendations, None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

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
        
        return jsonify({
            'original_article': {
                'title': title,
                'link': data.loc[indices[title], 'link'],
                'summary': data.loc[indices[title], 'summary']
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
    
    # Filter articles that contain the query
    matching_articles = data[data['title'].str.lower().str.contains(query, na=False)]
    
    results = []
    for _, row in matching_articles.head(10).iterrows():
        results.append({
            'title': row['title'],
            'summary': row['summary'][:200] + '...' if len(row['summary']) > 200 else row['summary'],
            'link': row['link']
        })
    
    return jsonify({'articles': results})

if __name__ == '__main__':
    print("Loading model...")
    load_model()
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000) 