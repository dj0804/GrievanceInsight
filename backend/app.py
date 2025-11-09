"""
FastAPI application for AI Grievance Summarizer API
Provides REST endpoints for complaint analysis and summarization.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
import io
import uvicorn
from grievance_summarizer import GrievanceSummarizer
from database_utils import db_manager, create_tables
import os

# Initialize FastAPI app
app = FastAPI(
    title="AI Grievance Summarizer API",
    description="AI-powered system for analyzing and summarizing hostel grievances",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the summarizer
summarizer = GrievanceSummarizer()

# Pydantic models for request/response
class ComplaintInput(BaseModel):
    raw_text: str

class ComplaintsBatch(BaseModel):
    complaints: List[ComplaintInput]

class DashboardResponse(BaseModel):
    total_complaints: int
    complaint_volume_by_category: Dict[str, int]
    sentiment_overview: Dict[str, int]
    urgency_distribution: Dict[str, int]
    weekly_summary: str
    top_recurring_issues: List[str]
    processed_complaints: Optional[List[Dict]] = None

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API health check."""
    return HealthResponse(
        status="healthy",
        message="AI Grievance Summarizer API is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Service is operational"
    )

@app.post("/analyze/batch", response_model=DashboardResponse)
async def analyze_complaints_batch(batch: ComplaintsBatch):
    """
    Analyze a batch of complaints and return dashboard insights.
    
    Args:
        batch: ComplaintsBatch object containing list of complaints
        
    Returns:
        DashboardResponse with analysis results
    """
    try:
        # Convert to list of dictionaries
        complaints_data = [{"raw_text": complaint.raw_text} for complaint in batch.complaints]
        
        if not complaints_data:
            raise HTTPException(status_code=400, detail="No complaints provided")
        
        # Process complaints
        results = summarizer.process_complaints(data=complaints_data)
        
        if not results:
            raise HTTPException(status_code=500, detail="Failed to process complaints")
        
        return DashboardResponse(**results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/analyze/csv", response_model=DashboardResponse)
async def analyze_complaints_csv(file: UploadFile = File(...)):
    """
    Analyze complaints from uploaded CSV file.
    
    Args:
        file: CSV file with complaints (must have 'raw_text' column)
        
    Returns:
        DashboardResponse with analysis results
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read CSV content
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        # Validate CSV structure
        if 'raw_text' not in df.columns and len(df.columns) > 0:
            # Assume first column contains complaints
            df.rename(columns={df.columns[0]: 'raw_text'}, inplace=True)
        
        if 'raw_text' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'raw_text' column")
        
        # Convert to list of dictionaries
        complaints_data = df[['raw_text']].to_dict('records')
        
        if not complaints_data:
            raise HTTPException(status_code=400, detail="No valid complaints found in CSV")
        
        # Process complaints
        results = summarizer.process_complaints(data=complaints_data)
        
        if not results:
            raise HTTPException(status_code=500, detail="Failed to process complaints")
        
        return DashboardResponse(**results)
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/analyze/single")
async def analyze_single_complaint(complaint: ComplaintInput):
    """
    Analyze a single complaint.
    
    Args:
        complaint: Single complaint text
        
    Returns:
        Analysis results for the single complaint
    """
    try:
        # Process single complaint
        results = summarizer.process_complaints(data=[{"raw_text": complaint.raw_text}])
        
        if not results:
            raise HTTPException(status_code=500, detail="Failed to process complaint")
        
        # Return simplified response for single complaint
        return {
            "complaint": complaint.raw_text,
            "category": results['processed_complaints'][0]['category'],
            "sentiment": results['processed_complaints'][0]['sentiment'],
            "urgency": results['processed_complaints'][0]['urgency'],
            "clean_text": results['processed_complaints'][0]['clean_text']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get available complaint categories."""
    return {"categories": summarizer.categories}

@app.get("/demo")
async def demo_analysis():
    """
    Demo endpoint with sample data for testing.
    
    Returns:
        DashboardResponse with analysis of sample complaints
    """
    try:
        from grievance_summarizer import create_sample_data
        
        sample_data = create_sample_data()
        results = summarizer.process_complaints(data=sample_data)
        
        if not results:
            raise HTTPException(status_code=500, detail="Failed to process demo data")
        
        return DashboardResponse(**results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo processing error: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        create_tables()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")

@app.get("/analytics/db")
async def get_database_analytics():
    """
    Get analytics from the database instead of processing demo data.
    
    Returns:
        DashboardResponse with analysis from stored data
    """
    try:
        # Get statistics from database
        stats = db_manager.get_grievance_stats()
        
        # Get recent grievances with analysis
        recent_grievances = db_manager.get_all_grievances_with_analysis()
        
        # Process grievances for response
        processed_complaints = []
        for grievance in recent_grievances:
            if grievance['category']:  # Only include analyzed grievances
                processed_complaints.append({
                    'id': grievance['id'],
                    'raw_text': grievance['raw_text'],
                    'clean_text': grievance['clean_text'],
                    'category': grievance['category'],
                    'sentiment': grievance['sentiment'],
                    'urgency': grievance['urgency'],
                    'submitted_at': grievance['submitted_at'].isoformat() if grievance['submitted_at'] else None,
                    'processed_at': grievance['processed_at'].isoformat() if grievance['processed_at'] else None,
                })
        
        # Generate top recurring issues from categories
        category_items = sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)
        top_recurring_issues = [category for category, count in category_items[:5]]
        
        # Generate weekly summary
        total = stats['total']
        negative_count = stats['sentiments'].get('negative', 0)
        high_urgency_count = stats['urgencies'].get('high', 0)
        
        weekly_summary = f"Database contains {total} total grievances. {negative_count} show negative sentiment, and {high_urgency_count} are marked as high urgency. Top categories: {', '.join(top_recurring_issues[:3])}."
        
        return DashboardResponse(
            total_complaints=total,
            complaint_volume_by_category=stats['categories'],
            sentiment_overview=stats['sentiments'],
            urgency_distribution=stats['urgencies'],
            weekly_summary=weekly_summary,
            top_recurring_issues=top_recurring_issues,
            processed_complaints=processed_complaints
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/analyze/single/db")
async def analyze_single_complaint_with_db(complaint: ComplaintInput):
    """
    Analyze a single complaint and store it in the database.
    
    Args:
        complaint: Single complaint text
        
    Returns:
        Analysis results with database ID
    """
    try:
        # Store the grievance in database first
        grievance_id = db_manager.insert_grievance(complaint.raw_text)
        
        # Process with AI
        results = summarizer.process_complaints(data=[{"raw_text": complaint.raw_text}])
        
        if not results or not results['processed_complaints']:
            raise HTTPException(status_code=500, detail="Failed to process complaint")
        
        analysis_data = results['processed_complaints'][0]
        
        # Store analysis result in database
        analysis_id = db_manager.insert_analysis_result(
            grievance_id=grievance_id,
            category=analysis_data['category'],
            sentiment=analysis_data['sentiment'],
            urgency=analysis_data['urgency'],
            clean_text=analysis_data['clean_text']
        )
        
        return {
            "grievance_id": grievance_id,
            "analysis_id": analysis_id,
            "complaint": complaint.raw_text,
            "category": analysis_data['category'],
            "sentiment": analysis_data['sentiment'],
            "urgency": analysis_data['urgency'],
            "clean_text": analysis_data['clean_text']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/grievances/recent")
async def get_recent_grievances(limit: int = 10):
    """
    Get recent grievances from the database.
    
    Args:
        limit: Number of grievances to return
        
    Returns:
        List of recent grievances with analysis
    """
    try:
        grievances = db_manager.get_recent_grievances(limit)
        
        # Format for response
        formatted_grievances = []
        for g in grievances:
            formatted_grievances.append({
                'id': g['id'],
                'raw_text': g['raw_text'],
                'category': g['category'],
                'sentiment': g['sentiment'],
                'urgency': g['urgency'],
                'clean_text': g['clean_text'],
                'submitted_at': g['submitted_at'].isoformat() if g['submitted_at'] else None
            })
        
        return {"grievances": formatted_grievances}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/grievances/search")
async def search_grievances(q: str):
    """
    Search grievances by text content.
    
    Args:
        q: Search query
        
    Returns:
        List of matching grievances
    """
    try:
        grievances = db_manager.search_grievances(q)
        
        # Format for response
        formatted_grievances = []
        for g in grievances:
            formatted_grievances.append({
                'id': g['id'],
                'raw_text': g['raw_text'],
                'category': g['category'],
                'sentiment': g['sentiment'],
                'urgency': g['urgency'],
                'clean_text': g['clean_text'],
                'submitted_at': g['submitted_at'].isoformat() if g['submitted_at'] else None
            })
        
        return {"grievances": formatted_grievances, "query": q}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
