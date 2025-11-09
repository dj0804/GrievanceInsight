"""
Database utility module for PostgreSQL integration
Provides functions to store and retrieve grievance data
"""

import os
import psycopg2
import psycopg2.extras
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'hostel_grievances'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password')
        }
        
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.connection_params)
    
    def insert_grievance(self, raw_text: str, user_info: Optional[Dict] = None, ip_address: Optional[str] = None) -> int:
        """
        Insert a new grievance and return the ID
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO user_grievances (raw_text, user_info, ip_address)
                VALUES (%s, %s, %s)
                RETURNING id
                """
                cursor.execute(query, (raw_text, json.dumps(user_info) if user_info else None, ip_address))
                return cursor.fetchone()[0]
    
    def insert_analysis_result(self, grievance_id: int, category: str, sentiment: str, 
                             urgency: str, clean_text: str, confidence: Optional[Dict] = None) -> int:
        """
        Insert analysis result for a grievance
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO analysis_results (grievance_id, category, sentiment, urgency, clean_text, confidence)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """
                cursor.execute(query, (
                    grievance_id, category, sentiment, urgency, clean_text,
                    json.dumps(confidence) if confidence else None
                ))
                return cursor.fetchone()[0]
    
    def insert_batch_summary(self, batch_data: Dict) -> int:
        """
        Insert batch processing summary
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO batch_summaries (
                    batch_name, total_complaints, complaint_volume_by_category,
                    sentiment_overview, urgency_distribution, weekly_summary,
                    top_recurring_issues, grievance_ids
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """
                cursor.execute(query, (
                    batch_data.get('batch_name'),
                    batch_data['total_complaints'],
                    json.dumps(batch_data['complaint_volume_by_category']),
                    json.dumps(batch_data['sentiment_overview']),
                    json.dumps(batch_data['urgency_distribution']),
                    batch_data['weekly_summary'],
                    json.dumps(batch_data['top_recurring_issues']),
                    json.dumps(batch_data.get('grievance_ids', []))
                ))
                return cursor.fetchone()[0]
    
    def get_grievance_stats(self) -> Dict:
        """
        Get comprehensive grievance statistics
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                # Total count
                cursor.execute("SELECT COUNT(*) as total FROM user_grievances")
                total = cursor.fetchone()['total']
                
                # Category distribution
                cursor.execute("""
                    SELECT category, COUNT(*) as count 
                    FROM analysis_results 
                    GROUP BY category
                """)
                categories = {row['category']: row['count'] for row in cursor.fetchall()}
                
                # Sentiment distribution
                cursor.execute("""
                    SELECT sentiment, COUNT(*) as count 
                    FROM analysis_results 
                    GROUP BY sentiment
                """)
                sentiments = {row['sentiment']: row['count'] for row in cursor.fetchall()}
                
                # Urgency distribution
                cursor.execute("""
                    SELECT urgency, COUNT(*) as count 
                    FROM analysis_results 
                    GROUP BY urgency
                """)
                urgencies = {row['urgency']: row['count'] for row in cursor.fetchall()}
                
                return {
                    'total': total,
                    'categories': categories,
                    'sentiments': sentiments,
                    'urgencies': urgencies
                }
    
    def get_all_grievances_with_analysis(self) -> List[Dict]:
        """
        Get all grievances with their analysis results
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                query = """
                SELECT 
                    g.id, g.raw_text, g.submitted_at, g.user_info, g.ip_address,
                    a.category, a.sentiment, a.urgency, a.clean_text, a.processed_at, a.confidence
                FROM user_grievances g
                LEFT JOIN analysis_results a ON g.id = a.grievance_id
                ORDER BY g.submitted_at DESC
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
    
    def get_recent_grievances(self, limit: int = 10) -> List[Dict]:
        """
        Get recent grievances with analysis
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                query = """
                SELECT 
                    g.id, g.raw_text, g.submitted_at,
                    a.category, a.sentiment, a.urgency, a.clean_text
                FROM user_grievances g
                LEFT JOIN analysis_results a ON g.id = a.grievance_id
                ORDER BY g.submitted_at DESC
                LIMIT %s
                """
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
    
    def search_grievances(self, search_term: str) -> List[Dict]:
        """
        Search grievances by text content
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                query = """
                SELECT 
                    g.id, g.raw_text, g.submitted_at,
                    a.category, a.sentiment, a.urgency, a.clean_text
                FROM user_grievances g
                LEFT JOIN analysis_results a ON g.id = a.grievance_id
                WHERE g.raw_text ILIKE %s
                ORDER BY g.submitted_at DESC
                """
                cursor.execute(query, (f'%{search_term}%',))
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
    
    def get_grievances_by_category(self, category: str) -> List[Dict]:
        """
        Get grievances filtered by category
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                query = """
                SELECT 
                    g.id, g.raw_text, g.submitted_at,
                    a.category, a.sentiment, a.urgency, a.clean_text
                FROM user_grievances g
                INNER JOIN analysis_results a ON g.id = a.grievance_id
                WHERE a.category = %s
                ORDER BY g.submitted_at DESC
                """
                cursor.execute(query, (category,))
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
    
    def get_latest_batch_summary(self) -> Optional[Dict]:
        """
        Get the most recent batch summary
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                query = """
                SELECT * FROM batch_summaries 
                ORDER BY created_at DESC 
                LIMIT 1
                """
                cursor.execute(query)
                row = cursor.fetchone()
                
                return dict(row) if row else None

# Global database manager instance
db_manager = DatabaseManager()


def create_tables():
    """
    Create database tables if they don't exist
    This function creates the same schema as defined in the Drizzle schema
    """
    with db_manager.get_connection() as conn:
        with conn.cursor() as cursor:
            # Create user_grievances table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_grievances (
                    id SERIAL PRIMARY KEY,
                    raw_text TEXT NOT NULL,
                    submitted_at TIMESTAMP DEFAULT NOW() NOT NULL,
                    user_info JSONB,
                    ip_address VARCHAR(45)
                )
            """)
            
            # Create analysis_results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id SERIAL PRIMARY KEY,
                    grievance_id INTEGER REFERENCES user_grievances(id) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    sentiment VARCHAR(50) NOT NULL,
                    urgency VARCHAR(50) NOT NULL,
                    clean_text TEXT NOT NULL,
                    confidence JSONB,
                    processed_at TIMESTAMP DEFAULT NOW() NOT NULL
                )
            """)
            
            # Create batch_summaries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS batch_summaries (
                    id SERIAL PRIMARY KEY,
                    batch_name VARCHAR(255),
                    total_complaints INTEGER NOT NULL,
                    complaint_volume_by_category JSONB NOT NULL,
                    sentiment_overview JSONB NOT NULL,
                    urgency_distribution JSONB NOT NULL,
                    weekly_summary TEXT NOT NULL,
                    top_recurring_issues JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                    grievance_ids JSONB
                )
            """)
            
            # Create system_analytics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_analytics (
                    id SERIAL PRIMARY KEY,
                    analytics_date TIMESTAMP DEFAULT NOW() NOT NULL,
                    total_grievances INTEGER NOT NULL,
                    category_counts JSONB NOT NULL,
                    sentiment_counts JSONB NOT NULL,
                    urgency_counts JSONB NOT NULL,
                    trending_issues JSONB,
                    weekly_growth JSONB
                )
            """)
            
            print("Database tables created successfully!")


if __name__ == "__main__":
    # Create tables when running this module directly
    create_tables()
