import asyncio
from typing import Dict, List, Any
from datetime import datetime
import json
import re
from dataclasses import dataclass

# Langgraph imports
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import TypedDict

# University database (in production, this would be a real database)
from university_database_mysql import university_db

class RecommendationState(TypedDict):
    student_profile: Dict[str, Any]
    cv_analysis: Dict[str, Any]
    university_matches: List[Dict[str, Any]]
    ai_analysis: str
    final_recommendations: List[Dict[str, Any]]
    processing_step: str

class UniversityRecommendationEngine:
    def __init__(self):
        # Initialize LLM (you'll need to set OPENROUTER_API_KEY environment variable)
        import os
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Warning: OpenRouter API key not set. Using mock responses.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model="openai/gpt-4",
                temperature=0.3,
                max_tokens=2000,
                openai_api_key=api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "University Recommender"
                }
            )
        
        # Initialize university database
        self.university_db = university_db
        
        # Build the Langgraph workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the Langgraph workflow for university recommendations
        """
        workflow = StateGraph(RecommendationState)
        
        # Add nodes
        workflow.add_node("analyze_profile", self._analyze_student_profile)
        workflow.add_node("match_universities", self._match_universities)
        workflow.add_node("score_matches", self._score_matches)
        workflow.add_node("generate_analysis", self._generate_ai_analysis)
        workflow.add_node("finalize_recommendations", self._finalize_recommendations)
        
        # Define the flow
        workflow.set_entry_point("analyze_profile")
        workflow.add_edge("analyze_profile", "match_universities")
        workflow.add_edge("match_universities", "score_matches")
        workflow.add_edge("score_matches", "generate_analysis")
        workflow.add_edge("generate_analysis", "finalize_recommendations")
        workflow.add_edge("finalize_recommendations", END)
        
        return workflow.compile()
    
    async def _analyze_student_profile(self, state: RecommendationState) -> RecommendationState:
        """
        Analyze student profile using LLM
        """
        profile = state["student_profile"]
        
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert university admissions counselor. Analyze the student profile and extract key insights.
            Focus on:
            1. Academic strength indicators
            2. Research alignment potential
            3. Geographic and cultural preferences
            4. Financial considerations
            5. Career trajectory alignment
            
            Provide a structured analysis that will help in university matching.
            """),
            ("human", "Student Profile: {profile}")
        ])
        
        if self.llm:
            response = await self.llm.ainvoke(
                analysis_prompt.format_messages(profile=json.dumps(profile, indent=2))
            )
            llm_insights = response.content
        else:
            llm_insights = "Mock analysis: Strong academic profile with clear research interests and well-defined career goals."
        
        # Parse the analysis
        analysis = {
            "academic_strength": self._extract_academic_strength(profile),
            "research_fit": profile.get("research_interests", ""),
            "geographic_preference": {
                "continent": profile.get("preferred_continent", ""),
                "country": profile.get("preferred_country", "")
            },
            "budget_category": profile.get("budget_preference", ""),
            "career_goal": profile.get("career_goal", ""),
            "llm_insights": llm_insights
        }
        
        state["cv_analysis"] = analysis
        state["processing_step"] = "profile_analyzed"
        return state
    
    async def _match_universities(self, state: RecommendationState) -> RecommendationState:
        """
        Match universities based on student profile
        """
        profile = state["student_profile"]
        analysis = state["cv_analysis"]
        
        # Get all universities from database
        all_universities = self.university_db.get_all_universities()
        
        # Filter based on basic criteria
        filtered_universities = []
        
        for uni in all_universities:
            # Geographic filtering
            if self._matches_geographic_preference(uni, analysis["geographic_preference"]):
                # Budget filtering
                if self._matches_budget_preference(uni, analysis["budget_category"]):
                    # Degree level filtering
                    if self._matches_degree_level(uni, profile.get("degree_level", "")):
                        filtered_universities.append(uni)
        
        state["university_matches"] = filtered_universities
        state["processing_step"] = "universities_matched"
        return state
    
    async def _score_matches(self, state: RecommendationState) -> RecommendationState:
        """
        Score university matches using AI
        """
        profile = state["student_profile"]
        universities = state["university_matches"]
        
        scoring_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert university matching algorithm. Score each university for this student profile.
            
            Scoring criteria (0-100):
            1. Academic fit (GPA, test scores vs requirements) - 25%
            2. Research alignment (student interests vs university strengths) - 30%
            3. Geographic preference match - 15%
            4. Financial feasibility - 20%
            5. Career goal alignment - 10%
            
            Return a JSON object with university_id and match_score for each university.
            """),
            ("human", "Student Profile: {profile}\n\nUniversities to score: {universities}")
        ])
        
        if self.llm:
            response = await self.llm.ainvoke(
                scoring_prompt.format_messages(
                    profile=json.dumps(profile, indent=2),
                    universities=json.dumps([{"id": u["id"], "name": u["name"], "country": u["country"]} for u in universities], indent=2)
                )
            )
            
            # Parse scores and apply to universities
            try:
                scores = json.loads(response.content)
                for uni in universities:
                    score_data = next((s for s in scores if s["university_id"] == uni["id"]), None)
                    uni["match_score"] = score_data["match_score"] if score_data else 50
            except:
                # Fallback scoring if LLM response parsing fails
                for i, uni in enumerate(universities):
                    uni["match_score"] = max(60, 95 - i * 5)  # Decreasing scores
        else:
            # Mock scoring when LLM is not available
            for i, uni in enumerate(universities):
                uni["match_score"] = max(60, 95 - i * 5)  # Decreasing scores
        
        # Sort by match score
        universities.sort(key=lambda x: x["match_score"], reverse=True)
        
        state["university_matches"] = universities[:10]  # Top 10 matches
        state["processing_step"] = "matches_scored"
        return state
    
    async def _generate_ai_analysis(self, state: RecommendationState) -> RecommendationState:
        """
        Generate comprehensive AI analysis and summary
        """
        profile = state["student_profile"]
        universities = state["university_matches"]
        
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert university admissions counselor providing personalized guidance.
            
            Generate a comprehensive analysis that includes:
            1. Profile Summary - student's academic strengths and background
            2. Geographic Alignment - how location preferences align with opportunities
            3. Financial Considerations - funding options and cost analysis
            4. Research Fit - alignment between interests and university programs
            5. Career Trajectory - how programs support career goals
            6. Application Strategy - specific advice for the application process
            7. Recommendations - why these specific universities are recommended
            
            Write in a professional, encouraging tone. Be specific and actionable.
            """),
            ("human", """
            Student Profile: {profile}
            
            Top University Matches: {universities}
            
            Generate a comprehensive analysis and recommendations.
            """)
        ])
        
        if self.llm:
            response = await self.llm.ainvoke(
                analysis_prompt.format_messages(
                    profile=json.dumps(profile, indent=2),
                    universities=json.dumps([{"name": u["name"], "country": u["country"], "match_score": u["match_score"]} for u in universities[:5]], indent=2)
                )
            )
            ai_analysis = response.content
        else:
            # Mock analysis when LLM is not available
            top_unis = [u["name"] for u in universities[:3]]
            ai_analysis = f"""**Profile Summary**: Based on your academic background and research interests, you present a strong candidate profile for graduate programs.

**Geographic Alignment**: Your preferences align well with top-tier institutions in your target regions.

**Financial Considerations**: Consider exploring funding opportunities including research assistantships and fellowships.

**Research Fit**: Your research interests show strong alignment with the programs at {', '.join(top_unis)}.

**Career Trajectory**: These programs will provide excellent preparation for your career goals.

**Application Strategy**: Focus on highlighting your research experience and academic achievements in your applications.

**Recommendations**: We recommend applying to {', '.join(top_unis)} as they offer the best match for your profile and goals."""
        
        state["ai_analysis"] = ai_analysis
        state["processing_step"] = "analysis_generated"
        return state
    
    async def _finalize_recommendations(self, state: RecommendationState) -> RecommendationState:
        """
        Finalize the recommendations
        """
        universities = state["university_matches"]
        
        # Take top 3 recommendations
        final_recommendations = universities[:3]
        
        state["final_recommendations"] = final_recommendations
        state["processing_step"] = "completed"
        return state
    
    def _extract_academic_strength(self, profile: Dict[str, Any]) -> str:
        """
        Extract academic strength indicators from profile
        """
        gpa = profile.get("gpa", "")
        test_scores = profile.get("test_scores", "")
        
        if gpa:
            try:
                gpa_value = float(gpa.split("/")[0])
                if gpa_value >= 3.7:
                    return "high"
                elif gpa_value >= 3.3:
                    return "medium"
                else:
                    return "developing"
            except:
                return "medium"
        return "medium"
    
    def _matches_geographic_preference(self, university: Dict[str, Any], geo_pref: Dict[str, str]) -> bool:
        """
        Check if university matches geographic preferences
        """
        # Comprehensive country-to-continent mapping <mcreference link="https://restcountries.com/" index="3">3</mcreference>
        country_to_continent = {
            # North America
            "united states": "north-america", "usa": "north-america", "america": "north-america",
            "canada": "north-america", "mexico": "north-america",
            
            # Europe
            "united kingdom": "europe", "uk": "europe", "britain": "europe", "england": "europe",
            "germany": "europe", "france": "europe", "italy": "europe", "spain": "europe",
            "netherlands": "europe", "belgium": "europe", "switzerland": "europe",
            "austria": "europe", "sweden": "europe", "norway": "europe", "denmark": "europe",
            "finland": "europe", "poland": "europe", "czech republic": "europe",
            "hungary": "europe", "portugal": "europe", "greece": "europe", "ireland": "europe",
            "romania": "europe", "bulgaria": "europe", "croatia": "europe", "slovenia": "europe",
            "slovakia": "europe", "estonia": "europe", "latvia": "europe", "lithuania": "europe",
            "luxembourg": "europe", "malta": "europe", "cyprus": "europe", "iceland": "europe",
            "russia": "europe", "ukraine": "europe", "belarus": "europe",
            
            # Asia
            "china": "asia", "japan": "asia", "south korea": "asia", "korea": "asia",
            "india": "asia", "singapore": "asia", "malaysia": "asia", "thailand": "asia",
            "vietnam": "asia", "philippines": "asia", "indonesia": "asia",
            "taiwan": "asia", "hong kong": "asia", "pakistan": "asia", "bangladesh": "asia",
            "sri lanka": "asia", "nepal": "asia", "myanmar": "asia", "cambodia": "asia",
            "laos": "asia", "brunei": "asia", "mongolia": "asia", "kazakhstan": "asia",
            "uzbekistan": "asia", "turkmenistan": "asia", "kyrgyzstan": "asia", "tajikistan": "asia",
            "afghanistan": "asia", "iran": "asia", "iraq": "asia", "turkey": "asia",
            "syria": "asia", "lebanon": "asia", "jordan": "asia", "israel": "asia",
            "palestine": "asia", "saudi arabia": "asia", "uae": "asia", "united arab emirates": "asia",
            "qatar": "asia", "kuwait": "asia", "bahrain": "asia", "oman": "asia", "yemen": "asia",
            
            # Australia/Oceania
            "australia": "australia", "new zealand": "australia", "fiji": "australia",
            "papua new guinea": "australia", "samoa": "australia", "tonga": "australia",
            "vanuatu": "australia", "solomon islands": "australia",
            
            # Africa
            "south africa": "africa", "egypt": "africa", "nigeria": "africa", "kenya": "africa",
            "ghana": "africa", "morocco": "africa", "tunisia": "africa", "algeria": "africa",
            "libya": "africa", "sudan": "africa", "ethiopia": "africa", "uganda": "africa",
            "tanzania": "africa", "zimbabwe": "africa", "botswana": "africa", "namibia": "africa",
            "zambia": "africa", "malawi": "africa", "mozambique": "africa", "madagascar": "africa",
            "mauritius": "africa", "seychelles": "africa", "rwanda": "africa", "burundi": "africa",
            "democratic republic of congo": "africa", "congo": "africa", "cameroon": "africa",
            "ivory coast": "africa", "senegal": "africa", "mali": "africa", "burkina faso": "africa",
            "niger": "africa", "chad": "africa", "central african republic": "africa",
            "gabon": "africa", "equatorial guinea": "africa", "sao tome and principe": "africa",
            "cape verde": "africa", "gambia": "africa", "guinea-bissau": "africa", "guinea": "africa",
            "sierra leone": "africa", "liberia": "africa", "togo": "africa", "benin": "africa",
            "angola": "africa", "lesotho": "africa", "swaziland": "africa", "eswatini": "africa",
            "comoros": "africa", "djibouti": "africa", "eritrea": "africa", "somalia": "africa",
            
            # South America
            "brazil": "south-america", "argentina": "south-america", "chile": "south-america",
            "colombia": "south-america", "peru": "south-america", "venezuela": "south-america",
            "ecuador": "south-america", "bolivia": "south-america", "paraguay": "south-america",
            "uruguay": "south-america", "guyana": "south-america", "suriname": "south-america",
            "french guiana": "south-america"
        }
        
        uni_country = university.get("country", "").lower().strip()
        pref_country = geo_pref.get("country", "")
        pref_continent = geo_pref.get("continent", "")
        
        # If country preference is specified and not "no-preference"
        if pref_country and pref_country != "no-preference":
            pref_country_normalized = pref_country.replace("-", " ").lower().strip()
            return pref_country_normalized in uni_country or uni_country in pref_country_normalized
        
        # If no country preference but continent preference is specified
        if pref_continent and pref_continent != "no-preference":
            # First try exact mapping
            uni_continent = country_to_continent.get(uni_country, "")
            if uni_continent:
                return uni_continent == pref_continent
            
            # Fallback: try partial matching for countries not in our mapping
            # This handles cases where country names might be slightly different
            for country_key, continent in country_to_continent.items():
                if (country_key in uni_country or uni_country in country_key) and continent == pref_continent:
                    return True
            
            # If still no match found, return False for continent filtering
            return False
        
        # If no preferences specified, match all
        return True
    
    def _matches_budget_preference(self, university: Dict[str, Any], budget_pref: str) -> bool:
        """
        Check if university matches budget preferences
        """
        if budget_pref == "self-funded":
            return True
        elif budget_pref in ["full-funding", "partial-funding"]:
            return university.get("scholarship_available", False)
        return True
    
    def _matches_degree_level(self, university: Dict[str, Any], degree_level: str) -> bool:
        """
        Check if university offers the desired degree level
        """
        # For now, assume all universities offer all degree levels
        # In a real system, this would check the university's program offerings
        return True
    
    async def generate_recommendations(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to generate university recommendations
        """
        initial_state = RecommendationState(
            student_profile=profile,
            cv_analysis={},
            university_matches=[],
            ai_analysis="",
            final_recommendations=[],
            processing_step="started"
        )
        
        # Run the workflow
        final_state = await self.workflow.ainvoke(initial_state)
        
        return {
            "universities": final_state["final_recommendations"],
            "ai_summary": final_state["ai_analysis"]
        }
    
    async def analyze_cv(self, cv_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Analyze uploaded CV content
        """
        # In a real implementation, you would:
        # 1. Extract text from PDF/DOC files
        # 2. Use NLP to extract relevant information
        # 3. Structure the extracted data
        
        # For now, return a mock analysis
        return {
            "filename": filename,
            "extracted_info": {
                "education": "Extracted education information",
                "experience": "Extracted work experience",
                "skills": "Extracted technical skills",
                "research": "Extracted research experience"
            },
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def get_all_universities(self) -> List[Dict[str, Any]]:
        """
        Get all universities from database
        """
        return self.university_db.get_all_universities()
    
    async def search_universities(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search universities by query
        """
        return self.university_db.search_universities(query, limit)