from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os
import json

app = Flask(__name__)
CORS(app)

# Global variables to store the model and data
data = None
tfidv = None
nmf = None
topics = None
cosine_sim = None
indices = None

def load_model():
    """Load the trained model and data"""
    global data, tfidv, nmf, topics, cosine_sim, indices
    
    try:
        # Load the dataset
        data = pd.read_csv('Dataset/result_final.csv')
        
        # Data cleaning
        data.dropna(how='any', subset=['title_summary'], inplace=True)
        data.drop_duplicates(subset=['title'], keep='first', inplace=True)
        data.drop_duplicates(subset=['summary'], keep='first', inplace=True)
        data.drop_duplicates(subset=['text'], keep='first', inplace=True)
        data.drop(labels=['Unnamed: 0', 'Unnamed: 0.1', 'title_summary'], axis=1, inplace=True)
        
        # Create soup for better recommendations
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
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def get_recommendations(title, num_recommendations=5):
    """Get article recommendations based on title"""
    try:
        if title not in indices:
            return None, "Title not found in dataset"
        
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations+1]
        
        news_indices = [i[0] for i in sim_scores]
        
        recommendations = []
        for i, idx in enumerate(news_indices):
            recommendation = {
                'rank': i + 1,
                'title': data['title'].iloc[idx],
                'summary': data['summary'].iloc[idx],
                'link': data['link'].iloc[idx],
                'date': str(data['date'].iloc[idx]) if pd.notna(data['date'].iloc[idx]) else 'N/A',
                'keywords': data['keywords'].iloc[idx],
                'similarity_score': float(sim_scores[i][1])
            }
            recommendations.append(recommendation)
        
        return recommendations, None
        
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get all available articles"""
    try:
        if data is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        articles = []
        for idx, row in data.head(50).iterrows():  # Limit to first 50 articles for performance
            article = {
                'id': int(idx),
                'title': row['title'],
                'summary': row['summary'][:200] + '...' if len(row['summary']) > 200 else row['summary'],
                'date': str(row['date']) if pd.notna(row['date']) else 'N/A'
            }
            articles.append(article)
        
        return jsonify({'articles': articles})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_articles():
    """Search articles by title"""
    try:
        if data is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'articles': []})
        
        # Simple search implementation
        matching_articles = []
        for idx, row in data.iterrows():
            if query in row['title'].lower() or query in row['summary'].lower():
                article = {
                    'id': int(idx),
                    'title': row['title'],
                    'summary': row['summary'][:200] + '...' if len(row['summary']) > 200 else row['summary'],
                    'date': str(row['date']) if pd.notna(row['date']) else 'N/A'
                }
                matching_articles.append(article)
                if len(matching_articles) >= 10:  # Limit results
                    break
        
        return jsonify({'articles': matching_articles})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_article_recommendations():
    """Get recommendations for a specific article"""
    try:
        if data is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        request_data = request.get_json()
        title = request_data.get('title')
        num_recommendations = request_data.get('num_recommendations', 5)
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        recommendations, error = get_recommendations(title, num_recommendations)
        
        if error:
            return jsonify({'error': error}), 404
        
        return jsonify({
            'original_article': {
                'title': title,
                'summary': data.loc[indices[title], 'summary'],
                'link': data.loc[indices[title], 'link'],
                'date': str(data.loc[indices[title], 'date']) if pd.notna(data.loc[indices[title], 'date']) else 'N/A'
            },
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': data is not None,
        'total_articles': len(data) if data is not None else 0
    })

if __name__ == '__main__':
    # Load the model when starting the app
    if load_model():
        print("Starting Flask app...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load model. Exiting...") 