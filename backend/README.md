# University Recommender Backend

AI-powered university recommendation system built with FastAPI and Langgraph.

## Features

- **AI-Powered Recommendations**: Uses Langgraph workflows with OpenAI GPT-4 for intelligent university matching
- **Student Profile Analysis**: Comprehensive analysis of academic profiles, research interests, and preferences
- **CV Processing**: Upload and analyze academic CVs/resumes
- **University Database**: Comprehensive database of top universities with detailed information
- **CORS Support**: Configured for seamless frontend integration
- **RESTful API**: Clean, documented API endpoints

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Langgraph**: Advanced workflow orchestration for AI agents
- **OpenAI GPT-4**: Large language model for intelligent analysis
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd university-recommender/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### Health Check
- **GET** `/` - Root endpoint with API information
- **GET** `/health` - Health check endpoint

### University Recommendations
- **POST** `/recommend` - Generate university recommendations
  ```json
  {
    "degree_level": "masters",
    "field_of_interest": "Natural Language Processing",
    "gpa": "3.78/4.00",
    "test_scores": "TOEFL 105, GRE 320",
    "preferred_continent": "north-america",
    "preferred_country": "united-states",
    "budget_preference": "partial-funding",
    "research_interests": "AI for healthcare, Ethical AI",
    "work_experience": "1 year RA at NLP lab",
    "language_preference": "english-only",
    "target_start_year": "2025",
    "study_mode": "on-campus",
    "career_goal": "industry"
  }
  ```

### CV Processing
- **POST** `/upload-cv` - Upload and analyze CV/resume
  - Accepts PDF, DOC, DOCX files
  - Maximum file size: 10MB

### University Data
- **GET** `/universities` - Get all universities
- **GET** `/universities/search?query=stanford&limit=10` - Search universities

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## Architecture

### Langgraph Workflow

The recommendation system uses a Langgraph workflow with the following steps:

1. **Profile Analysis**: Analyze student academic profile and extract key insights
2. **University Matching**: Filter universities based on basic criteria
3. **Scoring**: Use AI to score university matches based on multiple factors
4. **AI Analysis**: Generate comprehensive analysis and recommendations
5. **Finalization**: Prepare final recommendations with top matches

### Key Components

- `main.py`: FastAPI application with API endpoints
- `recommendation_engine.py`: Langgraph workflow for AI-powered recommendations
- `university_database.py`: University data management
- `requirements.txt`: Python dependencies

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FASTAPI_HOST`: Host to bind the server (default: 0.0.0.0)
- `FASTAPI_PORT`: Port to run the server (default: 8000)
- `ALLOWED_ORIGINS`: CORS allowed origins (default: localhost:3000)
- `LOG_LEVEL`: Logging level (default: INFO)

### CORS Configuration

The API is configured to allow requests from:
- http://localhost:3000 (Next.js development server)
- http://127.0.0.1:3000

To add more origins, update the `ALLOWED_ORIGINS` environment variable.

## Development

### Running in Development Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reloading when code changes.

### Testing

```bash
pytest
```

### Adding New Universities

To add new universities, update the `university_database.py` file or implement a proper database connection.

## Production Deployment

### Using Docker (Recommended)

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Build and run:
   ```bash
   docker build -t university-recommender-backend .
   docker run -p 8000:8000 --env-file .env university-recommender-backend
   ```

### Using a Process Manager

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Ensure your OpenAI API key is correctly set in the `.env` file
   - Check that you have sufficient credits in your OpenAI account

2. **CORS Errors**:
   - Verify that your frontend URL is included in `ALLOWED_ORIGINS`
   - Check that the frontend is making requests to the correct backend URL

3. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're using the correct Python version (3.8+)

4. **Port Already in Use**:
   - Change the port in the `.env` file or when running uvicorn
   - Kill any existing processes using the port

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.