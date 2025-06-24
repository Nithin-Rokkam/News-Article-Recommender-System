# News Article Recommender System

A modern, AI-powered news recommendation system that uses advanced machine learning techniques to suggest personalized articles based on content similarity.

## 🚀 Features

- **Content-Based Recommendations**: Uses TF-IDF vectorization and cosine similarity
- **Topic Modeling**: NMF (Non-negative Matrix Factorization) for topic discovery
- **Modern Web Interface**: Responsive design with Bootstrap 5
- **Real-time Search**: Search articles by title or content
- **Similarity Scoring**: Visual similarity scores for recommendations
- **Docker Support**: Easy containerization and deployment
- **Vercel Ready**: Serverless deployment configuration

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Machine Learning**: scikit-learn, pandas, numpy
- **Deployment**: Docker, Vercel
- **Data Processing**: TF-IDF, NMF, Cosine Similarity

## 📊 How It Works

1. **Data Preprocessing**: Cleans and prepares news article data
2. **Feature Extraction**: Converts text to numerical features using TF-IDF
3. **Topic Modeling**: Identifies underlying topics using NMF
4. **Similarity Calculation**: Computes cosine similarity between articles
5. **Recommendation Engine**: Suggests similar articles based on content

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker (optional)
- Vercel CLI (for Vercel deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd News-Article-Recommender-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   Open your browser and go to `http://localhost:5000`

### Using Docker directly

1. **Build the Docker image**
   ```bash
   docker build -t news-recommender .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 -v $(pwd)/Dataset:/app/Dataset news-recommender
   ```

## ☁️ Vercel Deployment

### Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

### Deploy to Vercel

1. **Deploy the application**
   ```bash
   vercel --prod
   ```

2. **Follow the prompts** to configure your deployment

3. **Access your deployed application** at the provided URL

### Environment Variables (Optional)

You can set environment variables in Vercel dashboard:
- `FLASK_ENV`: Set to `production` for production deployment

## 📁 Project Structure

```
News-Article-Recommender-System/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── vercel.json          # Vercel deployment configuration
├── runtime.txt          # Python runtime specification
├── .dockerignore        # Docker ignore file
├── templates/
│   └── index.html       # Main web interface
├── Dataset/
│   └── result_final.csv # News dataset
├── Model/
│   └── News_Article_recommender-system.ipynb # Jupyter notebook
└── README.md            # This file
```

## 🔧 API Endpoints

### Health Check
- **GET** `/api/health`
- Returns system health status

### Get Articles
- **GET** `/api/articles`
- Returns list of available articles

### Search Articles
- **GET** `/api/search?q=<query>`
- Search articles by title or content

### Get Recommendations
- **POST** `/api/recommendations`
- Body: `{"title": "article_title", "num_recommendations": 5}`
- Returns article recommendations

## 🎯 Usage

1. **Browse Articles**: View available articles on the homepage
2. **Search**: Use the search bar to find specific articles
3. **Get Recommendations**: Select an article to see similar recommendations
4. **View Details**: Click on article links to read full content

## 📈 Performance

- **Model Loading**: ~30-60 seconds on first startup
- **Recommendation Generation**: <1 second
- **Search Response**: <500ms
- **Memory Usage**: ~500MB-1GB (depending on dataset size)

## 🔍 Model Details

### Content-Based Filtering
- Uses TF-IDF vectorization for text feature extraction
- Implements NMF for topic modeling (20 topics)
- Calculates cosine similarity between articles
- Provides similarity scores for transparency

### Data Processing
- Removes duplicates and missing values
- Combines title, keywords, summary, and text for robust recommendations
- Handles timezone-aware date parsing

## 🛡️ Security

- CORS enabled for cross-origin requests
- Input validation and sanitization
- Error handling and logging
- Non-root Docker user

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Microsoft News Dataset (MIND) for the training data
- scikit-learn for machine learning algorithms
- Bootstrap for the responsive UI framework
- Flask for the web framework

## 📞 Support

For questions or issues:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

---

**Built with ❤️ using Flask and Machine Learning**
