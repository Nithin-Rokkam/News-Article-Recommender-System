# News Article Recommender System - Frontend

A modern, responsive web application that provides an intuitive interface for the news article recommender system. This frontend allows users to search for articles and get AI-powered recommendations based on content similarity.

## Features

- 🎨 **Modern UI/UX**: Beautiful, responsive design with smooth animations
- 🔍 **Smart Search**: Real-time search with dropdown suggestions
- 🤖 **AI Recommendations**: Content-based recommendations using TF-IDF and cosine similarity
- 📊 **Live Statistics**: Real-time display of recommendation metrics
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- ⚡ **Fast Performance**: Optimized loading and caching

## Technology Stack

### Backend
- **Flask**: Python web framework
- **scikit-learn**: Machine learning library for TF-IDF and similarity calculations
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive functionality
- **Bootstrap 5**: Responsive grid system and components
- **Font Awesome**: Icons

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## How It Works

### 1. Content-Based Recommendation System
The system uses the following approach:
- **TF-IDF Vectorization**: Converts article text into numerical vectors
- **NMF (Non-negative Matrix Factorization)**: Reduces dimensionality and finds topics
- **Cosine Similarity**: Calculates similarity between articles
- **Ranking**: Returns the most similar articles

### 2. User Interface Flow
1. **Search**: Users can search for articles by title
2. **Selection**: Choose an article from the dropdown suggestions
3. **Analysis**: The system analyzes the selected article's content
4. **Recommendations**: Displays similar articles with similarity scores
5. **Navigation**: Users can click links to read the original articles

### 3. API Endpoints

#### GET `/api/articles`
Returns all available article titles for search functionality.

#### POST `/api/recommendations`
Accepts a JSON payload with:
```json
{
    "title": "Article title",
    "num_recommendations": 5
}
```
Returns recommendations with similarity scores.

#### GET `/api/search?q=query`
Searches articles by title and returns matching results.

## File Structure

```
News-Article-Recommender-System/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Main HTML template
├── static/                        # Static assets (CSS, JS, images)
├── Dataset/
│   └── result_final.csv          # News articles dataset
├── Model/
│   └── News_Article_recommender-system.ipynb  # Original ML model
└── README_FRONTEND.md             # This file
```

## Customization

### Styling
The application uses CSS custom properties for easy theming. Modify the `:root` variables in `templates/index.html`:

```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --accent-color: #e74c3c;
    --light-bg: #ecf0f1;
    --dark-text: #2c3e50;
}
```

### Number of Recommendations
Change the default number of recommendations by modifying the `num_recommendations` parameter in the JavaScript `searchArticles()` function.

### Model Parameters
Adjust the ML model parameters in `app.py`:
- `n_components=20` in NMF for topic modeling
- TF-IDF parameters for vectorization
- Similarity calculation method

## Performance Optimization

### For Large Datasets
1. **Caching**: Implement Redis for caching recommendations
2. **Database**: Use PostgreSQL instead of loading CSV in memory
3. **Async Processing**: Use Celery for background recommendation generation
4. **CDN**: Serve static assets through a CDN

### For Production Deployment
1. **WSGI Server**: Use Gunicorn or uWSGI
2. **Environment Variables**: Configure production settings
3. **Logging**: Implement proper logging
4. **Monitoring**: Add health checks and metrics

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies with `pip install -r requirements.txt`

2. **Dataset not found**: Ensure `Dataset/result_final.csv` exists in the project directory

3. **Port already in use**: Change the port in `app.py` or kill the process using the port

4. **Memory issues**: For large datasets, consider using a database instead of loading everything in memory

### Debug Mode
Run the application in debug mode for detailed error messages:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the News Article Recommender System. Please refer to the main project license.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the original ML model notebook
3. Create an issue in the repository

---

**Happy Recommending! 🚀** 