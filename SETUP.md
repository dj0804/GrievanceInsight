# Hostel Grievance Summarizer

A modern web application for collecting, analyzing, and summarizing hostel grievances using AI, powered by Next.js Server Actions and Neon PostgreSQL.

## 🏗️ Architecture

### Server Actions + API Routes Hybrid
- **Server Actions**: All database operations (fast, type-safe, server-side)
- **API Routes**: Python script interactions only (external service integration)
- **Benefits**: Best performance for database, flexible AI service integration

## 🚀 Quick Setup

### 1. Database Setup (Neon PostgreSQL)

✅ **Database Status**: Connected to Neon PostgreSQL  
✅ **Tables Created**: `user_grievances`, `analysis_results`, `batch_summaries`, `system_analytics`
✅ **Server Actions**: Ready for database operations

### 2. Frontend Setup

```bash
cd hostel-portal
npm install
npm run dev      # Start frontend on http://localhost:3000
```

### 3. Backend Setup (Optional - for AI analysis)

```bash
cd backend
./start_backend.sh   # Setup venv, install deps, start API on :8000
```

## 📁 Project Structure

```
hostel-grievance-summariser/
├── hostel-portal/          # Next.js frontend application
│   ├── app/
│   │   ├── actions/        # 🔥 Server Actions (Database Operations)
│   │   │   ├── grievance-actions.ts
│   │   │   └── analytics-actions.ts
│   │   ├── api/            # � API Routes (Python Integration Only)
│   │   │   ├── ai/analyze/ # AI analysis endpoints
│   │   │   ├── grievances/ # External API compatibility
│   │   │   └── analytics/  # Analytics API (calls server action)
│   │   ├── submit/         # ✨ Uses server actions for submissions
│   │   └── admin/          # 📊 Uses server actions for analytics
│   ├── db/                 # 🗄️ Database configuration (Neon)
│   └── .env.local          # 🔑 Environment variables
├── backend/                # 🤖 Python AI backend
│   ├── app.py              # FastAPI server
│   ├── ai_summarizer.py    # AI analysis logic
│   ├── requirements.txt    # Python dependencies
│   └── start_backend.sh    # 🚀 Backend startup script
└── .env                    # 🌍 Global environment variables
```

## ✨ Features

### 🔥 Server Actions (Database)
- **Submit Grievances**: Direct server-side database operations
- **Analytics**: Fast, cached analytics data
- **Type Safety**: Full TypeScript support
- **Auto-revalidation**: Automatic UI updates
- **Performance**: Server-side execution

### 🤖 AI Analysis (API Routes)
- **External Service**: Python backend integration
- **Graceful Degradation**: Works without AI service
- **Status Monitoring**: AI service health checks
- **Batch Processing**: CSV upload support

## 🔧 Usage Examples

### Server Action (Database Operations)
```tsx
'use client';
import { submitGrievanceAction } from '@/app/actions/grievance-actions';

const handleSubmit = async (formData: FormData) => {
  const result = await submitGrievanceAction(formData);
  if (result.success) {
    // Handle success - automatic revalidation
  }
};
```

### API Route (Python Integration)
```tsx
const analyzeText = async (text: string) => {
  const response = await fetch('/api/ai/analyze', {
    method: 'POST',
    body: JSON.stringify({ raw_text: text })
  });
  return response.json();
};
```

## 🔧 Configuration

### Environment Variables

**Frontend (`.env.local`):**
```env
DATABASE_URL="postgresql://neondb_owner:npg_2zMLuWY6sqlk@ep-curly-night-adng21zf-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
PYTHON_BACKEND_URL=http://localhost:8000
```

## 📊 Available Operations

### Server Actions (Database)
- `submitGrievanceAction()` - Store new grievances
- `getAnalyticsAction()` - Get analytics data  
- `storeAnalysisResultAction()` - Store AI results
- `storeBatchSummaryAction()` - Store batch summaries

### API Routes (Python Only)
- `POST /api/ai/analyze` - Trigger AI analysis
- `GET /api/ai/analyze` - Check AI service status
- `POST /api/grievances/csv` - CSV batch processing
- `POST /api/grievances` - External API compatibility

## 🚀 How It Works

1. **Submit Grievance**: Uses server action → Direct database insert
2. **AI Analysis**: Optional API call to Python backend
3. **Store Results**: Server action stores AI analysis results
4. **Analytics**: Server action retrieves cached analytics
5. **UI Updates**: Automatic revalidation updates interface

## 🛠️ Troubleshooting

### Database (Neon)
- ✅ **Serverless**: No local PostgreSQL setup needed
- 🔍 **Test Connection**: Server actions handle connection testing
- �️ **Tables**: Auto-created via migrations

### AI Backend (Optional)
- 🔍 **Check Status**: `GET /api/ai/analyze`
- 🚀 **Start Backend**: `cd backend && ./start_backend.sh`
- 📊 **Works Without**: App functions without AI service

### Performance
- ⚡ **Fast Database**: Server actions execute server-side
- 🎯 **Targeted APIs**: Only Python interactions use API routes
- 🔄 **Auto-caching**: Built-in Next.js revalidation

## 🎯 Architecture Benefits

### Why Server Actions for Database?
- ✅ **Type Safety**: Full TypeScript integration
- ✅ **Performance**: Server-side execution
- ✅ **Caching**: Automatic revalidation
- ✅ **Security**: No exposed credentials
- ✅ **Simplicity**: Direct function calls

### Why API Routes for Python?
- ✅ **Service Separation**: Clear boundaries
- ✅ **External Access**: RESTful endpoints
- ✅ **Independence**: Services can scale separately
- ✅ **Compatibility**: Third-party integrations

The application now provides optimal performance with server actions for database operations while maintaining flexibility for AI service integration through targeted API routes! 🎉
