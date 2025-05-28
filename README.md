# University Recommender

A comprehensive university recommendation system that helps students find the best universities based on their preferences, academic background, and career goals. The system uses AI-powered analysis to provide personalized recommendations.

## Features

### 🎯 Personalized Recommendations
- AI-powered university matching based on student preferences
- Comprehensive filtering by country, field of study, and target start year
- Dynamic year selection (current year + 10 years)

### 📊 Rich University Data
- Extensive database of universities worldwide
- QS Rankings integration
- Detailed university information including:
  - Academic programs and fields of study
  - Location and country information
  - Rankings and reputation metrics
  - University descriptions and key features

### 🌐 Modern Web Interface
- Responsive Next.js frontend with TypeScript
- Clean, intuitive user interface
- Dynamic dropdowns with consistent styling
- Real-time data fetching and updates

### 🤖 AI Integration
- GPT-powered university analysis and enhancement
- Intelligent country and field consolidation
- Smart recommendation algorithms

## Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/ui** - Modern UI components
- **React Hooks** - State management and effects

### Backend
- **FastAPI** - Modern Python web framework
- **MySQL** - Relational database for university data
- **Python 3.13** - Core backend language
- **Uvicorn** - ASGI server for FastAPI

### Data & AI
- **OpenAI GPT** - AI-powered recommendations and analysis
- **QS Rankings API** - University ranking data
- **CSV Data Processing** - University database management
- **MySQL Connector** - Database connectivity
- **Langgraph** - Utilized for building robust and stateful multi-agent applications

## Project Structure

```
university-recommender/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # App Router pages and layouts
│   ├── components/          # Reusable UI components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utility functions
│   └── public/             # Static assets
├── backend/                 # FastAPI backend application
│   ├── main.py             # FastAPI application entry point
│   ├── university_database_mysql.py  # Database operations
│   ├── recommendation_engine.py      # AI recommendation logic
│   ├── gpt_university_enhancer.py    # GPT integration
│   ├── qs_rankings_scraper.py        # QS Rankings data fetching
│   └── requirements.txt    # Python dependencies
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.13+
- MySQL database
- OpenAI API key (for AI features)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

5. **Set up MySQL database:**
   - Create a MySQL database
   - Update database credentials in `.env`
   - Run data import scripts if needed

6. **Start the backend server:**
   ```bash
   python3 main.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   # or
   pnpm dev
   ```
   The application will be available at `http://localhost:3000`

## API Endpoints

### Core Endpoints
- `GET /` - API health check
- `GET /countries` - Get all available countries (consolidated)
- `GET /fields` - Get all fields of study (grouped)
- `POST /recommend` - Get university recommendations

### Data Management
- University data fetching and processing
- QS Rankings integration
- Country and field consolidation



## Development

### Code Style
- Frontend: ESLint + Prettier for TypeScript/React
- Backend: Black + isort for Python formatting
- Consistent naming conventions across the stack


## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support, please open an issue in the GitHub repository.