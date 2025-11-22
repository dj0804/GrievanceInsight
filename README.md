# AI Grievance Summarizer System

A comprehensive AI-powered system for analyzing and managing hostel grievances. This system includes both a FastAPI backend for AI processing and a Next.js frontend for user interaction.

Made by Dev Jain and Avadhoot Mahadik :)

## 🏗️ System Architecture

- **Backend API**: FastAPI server with AI-powered analysis (Python)
- **Frontend Portal**: Next.js web application for users and administrators (TypeScript/React)
- **AI Processing**: Transformer models for sentiment analysis and categorization
- **Data Analysis**: Pandas for trend extraction and statistical analysis

## 🚀 Features

### Backend API
- **AI-Powered Analysis**: Uses transformer models for sentiment analysis and text summarization
- **Automatic Categorization**: Classifies complaints into Hostel, Mess, Academics, and Administration categories
- **Trend Extraction**: Identifies recurring issues and patterns in complaints
- **Multiple Input Formats**: Supports single complaints, batch processing, and CSV file uploads
- **RESTful API**: Easy integration with web applications and dashboards
- **Real-time Processing**: Fast analysis with caching for better performance

### Frontend Portal
- **User Interface**: Clean, responsive design for grievance submission
- **Admin Dashboard**: Comprehensive analytics and complaint management
- **Real-time Analysis**: Instant feedback on submitted complaints
- **CSV Upload**: Batch processing capability for administrators
- **Data Visualization**: Charts and statistics for complaint trends

## 📋 Requirements

- Python 3.8+ (for backend)
- Node.js 18+ (for frontend)
- Virtual environment (recommended)

## 🔧 Installation

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hostel-grievance-summariser
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd hostel-portal
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

## 🚀 Quick Start

### Option 1: Using Start Scripts

**Start Backend API**:
```bash
./start_api.sh
```

**Start Frontend Portal** (in a new terminal):
```bash
./start_frontend.sh
```

### Option 2: Manual Start

**Backend**:
```bash
python app.py
```

**Frontend**:
```bash
cd hostel-portal
npm run dev
```

### Access the System

- **Frontend Portal**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 Frontend Pages

- **Home** (`/`): System overview and navigation
- **Submit Grievance** (`/submit`): User form for complaint submission
- **Admin Dashboard** (`/admin`): Analytics and complaint management
- **About** (`/about`): System information and documentation

## 📊 API Endpoints

### Health Check
- **GET** `/` - Root endpoint
- **GET** `/health` - Health check

### Analysis Endpoints

#### 1. Analyze Single Complaint
**POST** `/analyze/single`

```json
{
  "raw_text": "The mess food is awful and uncooked. Please check quality control."
}
```

**Response**:
```json
{
  "complaint": "The mess food is awful and uncooked...",
  "category": "Mess",
  "sentiment": "Negative",
  "urgency": "High",
  "clean_text": "the mess food is awful and uncooked..."
}
```

#### 2. Analyze Batch of Complaints
**POST** `/analyze/batch`

```json
{
  "complaints": [
    {"raw_text": "Hostel room fan not working"},
    {"raw_text": "Food quality is poor in mess"},
    {"raw_text": "Need grade verification for course"}
  ]
}
```

**Response**:
```json
{
  "total_complaints": 3,
  "complaint_volume_by_category": {
    "Hostel": 1,
    "Mess": 1,
    "Academics": 1
  },
  "sentiment_overview": {
    "Negative": 3
  },
  "urgency_distribution": {
    "High": 1,
    "Medium": 2
  },
  "weekly_summary": "Analysis shows issues across hostel maintenance, food quality...",
  "top_recurring_issues": [
    "Frequent topic: 'Quality' (mentioned 2 times)",
    "Frequent topic: 'Food' (mentioned 1 times)"
  ]
}
```

#### 3. Analyze CSV File
**POST** `/analyze/csv`

Upload a CSV file with complaints. The CSV should have a `raw_text` column or the first column will be treated as complaint text.

#### 4. Demo Analysis
**GET** `/demo`

Returns analysis results using sample complaint data for testing.

#### 5. Get Categories
**GET** `/categories`

Returns available complaint categories:
```json
{
  "categories": ["Hostel", "Mess", "Academics", "Administration"]
}
```

## 🔧 Configuration

### Environment Variables

You can configure the API using environment variables:

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export LOG_LEVEL=info
```

### Custom Configuration

For production deployment, modify the configuration in `app.py`:

```python
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 📁 Project Structure

```
hostel-grievance-summariser/
├── app.py                    # FastAPI application
├── grievance_summarizer.py   # Core analysis engine
├── requirements.txt          # Dependencies
├── README.md                # Documentation
├── .gitignore               # Git ignore rules
└── .venv/                   # Virtual environment
```

## 🧪 Testing

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Demo analysis
curl http://localhost:8000/demo

# Single complaint analysis
curl -X POST "http://localhost:8000/analyze/single" \
     -H "Content-Type: application/json" \
     -d '{"raw_text": "The hostel WiFi is not working properly"}'

# Batch analysis
curl -X POST "http://localhost:8000/analyze/batch" \
     -H "Content-Type: application/json" \
     -d '{
       "complaints": [
         {"raw_text": "Mess food quality is poor"},
         {"raw_text": "Room cleaning not done regularly"}
       ]
     }'
```

### Test with Python

```python
import requests

# Single complaint
response = requests.post(
    "http://localhost:8000/analyze/single",
    json={"raw_text": "The mess food is terrible"}
)
print(response.json())

# Batch analysis
response = requests.post(
    "http://localhost:8000/analyze/batch",
    json={
        "complaints": [
            {"raw_text": "Hostel AC not working"},
            {"raw_text": "Food quality issues in mess"}
        ]
    }
)
print(response.json())
```

## 🚀 Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables for Production

```bash
export TRANSFORMERS_CACHE=/app/cache
export TOKENIZERS_PARALLELISM=false
export LOG_LEVEL=warning
```

## 🔒 Security Considerations

1. **CORS Configuration**: Restrict origins in production
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **Input Validation**: All inputs are validated using Pydantic models
4. **File Upload Security**: CSV uploads are validated and processed safely
5. **Error Handling**: Detailed error messages are logged but not exposed to clients

## 🤝 Integration Examples

### Frontend Integration (JavaScript)

```javascript
// Analyze complaints
async function analyzeComplaints(complaints) {
    const response = await fetch('http://localhost:8000/analyze/batch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            complaints: complaints.map(text => ({raw_text: text}))
        })
    });
    
    return await response.json();
}

// Usage
const results = await analyzeComplaints([
    "Hostel WiFi is down",
    "Food quality needs improvement"
]);
console.log(results);
```

### Dashboard Integration

The API provides structured data perfect for dashboard visualization:

- **Category Distribution**: Use `complaint_volume_by_category` for pie charts
- **Sentiment Analysis**: Use `sentiment_overview` for sentiment distribution
- **Trends**: Use `top_recurring_issues` for trending topics
- **Summary**: Use `weekly_summary` for executive summary

## 📈 Performance

- **Processing Speed**: ~100-500 complaints per minute (depending on hardware)
- **Memory Usage**: ~2-4GB RAM for transformer models
- **Scalability**: Horizontal scaling supported with load balancers

## 🐛 Troubleshooting

### Common Issues

1. **Model Download Timeout**: First run may take time to download AI models
2. **Memory Issues**: Ensure sufficient RAM (4GB+) for transformer models
3. **CORS Errors**: Configure CORS settings for your frontend domain

### Logs

The API provides detailed logging. Check console output for debugging information.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting section above
