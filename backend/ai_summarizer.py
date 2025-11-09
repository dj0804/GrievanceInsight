# AI Grievance Summarizer - Standalone Script
import pandas as pd
import numpy as np
from collections import Counter
import re

# Define Global Constants
CATEGORIES = ['Hostel', 'Mess', 'Academics', 'Administration']

# Basic stopwords list
ENGLISH_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
    'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after', 'above', 
    'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
    'further', 'then', 'once', 'to'
}

# Simple tokenization function
def simple_word_tokenize(text):
    """Simple word tokenization using regex"""
    return re.findall(r'\b\w+\b', text.lower())

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies cleaning and normalization steps: removes duplicates, anonymizes, 
    and normalizes text.
    """
    print("Step 1: Data Cleaning...")
    # a. Remove duplicate complaints
    df.drop_duplicates(subset=['raw_text'], inplace=True)
    
    # b. Anonymize (Placeholder: simple lowercase/string conversion)
    def anonymize_text(text):
        if pd.isna(text): return ""
        return str(text).lower() 
        
    df['clean_text'] = df['raw_text'].apply(anonymize_text)
    
    # c. Normalize text (remove extra spaces)
    df['clean_text'] = df['clean_text'].str.strip()
    return df

def load_classification_model():
    """Placeholder for loading a trained scikit-learn classification model."""
    # In a real project, the model and vectorizer would be loaded here.
    return None 

def classify_complaints(df: pd.DataFrame, classifier=None) -> pd.DataFrame:
    """
    Classifies complaints into defined categories. Uses simulation if no model is provided.
    """
    print("Step 2: Complaint Classification (Simulated)...")
    if classifier:
        # Actual model prediction code goes here
        pass
    
    # Simulating classification 
    weights = [0.35, 0.35, 0.15, 0.15] # Mess and Hostel often have more complaints
    df['category'] = np.random.choice(CATEGORIES, size=len(df), p=weights) 
    return df

def perform_sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes the emotional tone of complaints. Uses simulation for portability.
    """
    print("Step 3: Sentiment Analysis (Simulated)...")
    
    try:
        # Try to use transformers if available
        from transformers import pipeline
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)
        
        def get_sentiment(text):
            if not text: return 'Neutral'
            try:
                result = sentiment_pipeline(text[:250])[0]
                return result['label'].capitalize()
            except Exception:
                return 'Neutral'

        df['sentiment'] = df['clean_text'].apply(get_sentiment)
        
    except Exception as e:
        print(f"Transformers not available, using simulation: {e}")
        # Fallback to simulation 
        df['sentiment'] = np.random.choice(['Negative', 'Neutral', 'Positive'], size=len(df), p=[0.7, 0.2, 0.1])

    # Placeholder for 'Urgency' assessment
    df['urgency'] = np.random.choice(['High', 'Medium', 'Low'], size=len(df), p=[0.2, 0.5, 0.3])
    return df

def summarize_and_extract_trends(df: pd.DataFrame) -> dict:
    """
    Identifies top recurring issues via frequency and generates a weekly summary.
    """
    print("Step 4: Summarization and Trend Extraction...")
    results = {}
    
    # a. Trend Extraction (Top 3 Recurring Issues)
    all_text = ' '.join(df['clean_text'].tolist())
    
    # Use simple tokenization function
    words = simple_word_tokenize(all_text)
    filtered_words = [w for w in words if w.isalnum() and w not in ENGLISH_STOPWORDS and len(w) > 2]
    
    # Use Counter for frequency analysis
    fdist = Counter(filtered_words)
    top_3_words = [item[0] for item in fdist.most_common(3)]
    
    results['top_recurring_issues'] = [
        f'Frequent topic: "{word.capitalize()}" (mentioned {fdist[word]} times)' 
        for word in top_3_words
    ]

    # b. Weekly Summarization 
    combined_complaints = ' '.join(df['clean_text'].tolist())
    
    try:
        # Try to use transformers for summarization
        from transformers import pipeline
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6", device=-1) 
        
        summary = summarizer(
            combined_complaints[:2000], 
            max_length=150, 
            min_length=30, 
            do_sample=False
        )[0]['summary_text']
        results['weekly_summary'] = summary
        
    except Exception as e:
        print(f"Transformers summarization not available, using fallback: {e}")
        # Fallback to placeholder summary
        results['weekly_summary'] = "The analysis indicates high volume complaints this week, primarily concerning food quality and hostel maintenance. Urgent action is required to address several critical water leaks and staff behavior in the administrative sector."
    
    return results

def run_ai_summarizer(file_path):
    """
    Main function to run the end-to-end process from file upload to dashboard data.
    """
    print("--- AI Grievance Summarizer Started ---")
    
    # 1. Admin Uploads Complaint Data (Reading a CSV)
    try:
        raw_df = pd.read_csv(file_path)
        # Assuming the first column contains the complaint content if not explicitly named
        if raw_df.columns[0] != 'raw_text':
             raw_df.rename(columns={raw_df.columns[0]: 'raw_text'}, inplace=True)
    except Exception as e:
        print(f"Error reading file: {e}. Please ensure the CSV file '{file_path}' exists and is formatted correctly.")
        return None

    # 2. Real-Time Processing (Backend workflow)
    classifier_model = load_classification_model()

    # Apply all processing steps
    processed_df = clean_data(raw_df.copy())
    processed_df = classify_complaints(processed_df, classifier_model)
    processed_df = perform_sentiment_analysis(processed_df)
    analysis_output = summarize_and_extract_trends(processed_df)
    
    # 3. Dashboard Visualization Data
    dashboard_data = {
        'complaint_volume_by_category': processed_df['category'].value_counts().to_dict(),
        'sentiment_overview': processed_df['sentiment'].value_counts().to_dict(),
        'top_complaints_summary': analysis_output['weekly_summary'],
        'top_recurring_issues_list': analysis_output['top_recurring_issues'],
        'raw_processed_data': processed_df.head().to_dict('records')
    }

    return dashboard_data

def display_dashboard(data: dict):
    """
    Displays the processed insights in a console-based format, simulating the
    Interactive Admin Dashboard Features.
    """
    print("\n=======================================================")
    print("### AI Grievance Summarizer Admin Dashboard Insights ###")
    print("=======================================================")
    
    # 1. Weekly Top Complaints Summary
    print("\n## 1. Weekly Insights Summary (Actionable Report)")
    print("-------------------------------------------------------")
    print(data['top_complaints_summary'])

    # 2. Complaint Volume by Category
    print("\n## 2. Complaint Volume by Category")
    print("-------------------------------------------------------")
    for cat, count in data['complaint_volume_by_category'].items():
        print(f"- {cat.ljust(15)}: {count} complaints")
    
    # 3. Top Recurring Issues
    print("\n## 3. Top Recurring Issues (Frequency Analysis)")
    print("-------------------------------------------------------")
    if data['top_recurring_issues_list']:
        for i, issue in enumerate(data['top_recurring_issues_list']):
            print(f"{i+1}. {issue}")
    else:
        print("No recurring issues detected this week.")
    
    # 4. Sentiment Overview
    print("\n## 4. Sentiment Distribution")
    print("-------------------------------------------------------")
    total_complaints = sum(data['sentiment_overview'].values())
    for sentiment, count in data['sentiment_overview'].items():
        percent = (count / total_complaints) * 100 if total_complaints else 0
        print(f"- {sentiment.ljust(10)}: {count} ({percent:.1f}%)")
    
    print("\n-------------------------------------------------------")
    print("--- Dashboard Display Complete ---")

if __name__ == "__main__":
    # Run the system
    final_output_data = run_ai_summarizer("weekly_complaints_dummy.csv")

    if final_output_data:
        display_dashboard(final_output_data)
    else:
        print("\nFailed to generate dashboard data.")
