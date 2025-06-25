from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Simple in-memory data for testing
sample_articles = [
    {
        'id': 1,
        'title': 'Sample News Article 1',
        'summary': 'This is a sample news article for testing the deployment.',
        'date': '2024-01-01'
    },
    {
        'id': 2,
        'title': 'Sample News Article 2',
        'summary': 'Another sample article to test the recommender system.',
        'date': '2024-01-02'
    },
    {
        'id': 3,
        'title': 'Sample News Article 3',
        'summary': 'Third sample article for deployment testing.',
        'date': '2024-01-03'
    }
]

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get all available articles"""
    try:
        return jsonify({'articles': sample_articles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_articles():
    """Search articles by title"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'articles': []})
        
        matching_articles = []
        for article in sample_articles:
            if query in article['title'].lower() or query in article['summary'].lower():
                matching_articles.append(article)
        
        return jsonify({'articles': matching_articles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_article_recommendations():
    """Get recommendations for a specific article"""
    try:
        request_data = request.get_json()
        title = request_data.get('title')
        num_recommendations = request_data.get('num_recommendations', 3)
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Simple recommendation logic
        recommendations = []
        for i, article in enumerate(sample_articles):
            if article['title'] != title and len(recommendations) < num_recommendations:
                recommendation = {
                    'rank': i + 1,
                    'title': article['title'],
                    'summary': article['summary'],
                    'link': f"https://example.com/article/{article['id']}",
                    'date': article['date'],
                    'keywords': 'sample, test, news',
                    'similarity_score': 0.8 - (i * 0.1)
                }
                recommendations.append(recommendation)
        
        return jsonify({
            'original_article': {
                'title': title,
                'summary': 'Sample article for testing',
                'link': 'https://example.com/article/1',
                'date': '2024-01-01'
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
        'model_loaded': True,
        'total_articles': len(sample_articles),
        'message': 'Simple deployment version working!'
    })

if __name__ == '__main__':
    print("Starting Flask app (simple version)...")
    app.run(debug=True, host='0.0.0.0', port=5000) 