#!/usr/bin/env python3
"""
Test script for the News Article Recommender System
"""

import requests
import json
import time
import sys

def test_health_endpoint(base_url):
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_articles_endpoint(base_url):
    """Test the articles endpoint"""
    print("Testing articles endpoint...")
    try:
        response = requests.get(f"{base_url}/api/articles")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Articles endpoint passed: {len(data.get('articles', []))} articles found")
            return True
        else:
            print(f"❌ Articles endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Articles endpoint error: {e}")
        return False

def test_search_endpoint(base_url):
    """Test the search endpoint"""
    print("Testing search endpoint...")
    try:
        response = requests.get(f"{base_url}/api/search?q=tech")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search endpoint passed: {len(data.get('articles', []))} results found")
            return True
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
        return False

def test_recommendations_endpoint(base_url):
    """Test the recommendations endpoint"""
    print("Testing recommendations endpoint...")
    try:
        # First get some articles to test with
        articles_response = requests.get(f"{base_url}/api/articles")
        if articles_response.status_code != 200:
            print("❌ Could not get articles for recommendation test")
            return False
        
        articles = articles_response.json().get('articles', [])
        if not articles:
            print("❌ No articles available for recommendation test")
            return False
        
        # Test with the first article
        test_article = articles[0]['title']
        payload = {
            "title": test_article,
            "num_recommendations": 3
        }
        
        response = requests.post(
            f"{base_url}/api/recommendations",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"✅ Recommendations endpoint passed: {len(recommendations)} recommendations found")
            return True
        else:
            print(f"❌ Recommendations endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Recommendations endpoint error: {e}")
        return False

def main():
    """Main test function"""
    base_url = "http://localhost:5000"
    
    print("🚀 Starting News Article Recommender System Tests")
    print("=" * 50)
    
    # Wait for the application to start
    print("⏳ Waiting for application to start...")
    time.sleep(5)
    
    tests = [
        test_health_endpoint,
        test_articles_endpoint,
        test_search_endpoint,
        test_recommendations_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test(base_url):
            passed += 1
        print("-" * 30)
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the application logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 