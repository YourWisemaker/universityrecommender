from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our recommendation engine and database
from recommendation_engine import UniversityRecommendationEngine
from university_database_mysql import university_db

app = FastAPI(
    title="University Recommendation API",
    description="AI-powered university recommendation system using Langgraph",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine
recommendation_engine = UniversityRecommendationEngine()

# Pydantic models for request/response
class StudentProfile(BaseModel):
    degree_level: str
    field_of_interest: str
    gpa: str
    test_scores: Optional[str] = None
    preferred_continent: str
    preferred_country: str
    budget_preference: str
    research_interests: str
    work_experience: str
    language_preference: str
    target_start_year: str
    study_mode: str
    career_goal: str

class University(BaseModel):
    id: int
    name: str
    country: str
    ranking: int
    match_score: float
    tuition_fee: str
    scholarship_available: bool
    program_name: str
    duration: str
    requirements: List[str]
    research_areas: List[str]
    faculty_highlights: List[str]
    campus_life: str
    application_deadline: str
    website: str
    description: str
    strengths: List[str]
    admission_rate: str

class RecommendationResponse(BaseModel):
    universities: List[University]
    ai_summary: str
    processing_time: float

@app.get("/")
async def root():
    return {
        "message": "University Recommendation API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/recommend")
async def recommend_universities(profile: StudentProfile):
    try:
        recommendations = await recommendation_engine.generate_recommendations(profile.dict())
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/top-universities/{field}")
async def get_top_universities(field: str, country: str = None):
    """Get top 3 universities for a specific field using AI"""
    try:
        top_universities = await university_db.generate_universities_for_field(field, country, 3)
        return {"top_universities": top_universities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-university")
async def generate_university(university_name: str, country: str, field: str = "Computer Science"):
    """Generate comprehensive university data using AI"""
    try:
        university_data = await university_db.generate_university_with_gpt(university_name, country, field)
        if university_data:
            return {"university": university_data}
        else:
            raise HTTPException(status_code=404, detail="Could not generate university data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload and process CV/Resume
    """
    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/msword", 
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload PDF, DOC, or DOCX files.")
        
        # Read file content
        content = await file.read()
        
        # Process CV using Langgraph (extract relevant information)
        cv_analysis = await recommendation_engine.analyze_cv(content, file.filename)
        
        return {
            "message": "CV uploaded and analyzed successfully",
            "filename": file.filename,
            "analysis": cv_analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

@app.get("/universities")
async def get_all_universities():
    """
    Get all available universities in the database
    """
    try:
        universities = await recommendation_engine.get_all_universities()
        return {"universities": universities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching universities: {str(e)}")

@app.get("/universities/search")
async def search_universities(query: str, limit: int = 10):
    """
    Search universities by name or other criteria
    """
    try:
        results = await recommendation_engine.search_universities(query, limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching universities: {str(e)}")

@app.get("/countries")
async def get_countries():
    """
    Get all available countries from the database
    """
    try:
        countries = await university_db.get_all_countries()
        return {"countries": countries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching countries: {str(e)}")

@app.get("/fields")
async def get_fields():
    """
    Get all available fields of study from the database
    """
    try:
        fields = await university_db.get_all_fields()
        return {"fields": fields}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching fields: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)