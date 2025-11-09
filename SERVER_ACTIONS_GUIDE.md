# Server Actions vs API Routes Architecture

This application now uses a clear separation between database operations and Python script interactions:

## 🏗️ Architecture Overview

### Server Actions (Database Operations)
- **Location**: `/app/actions/`
- **Purpose**: All database CRUD operations
- **Benefits**: 
  - Server-side execution
  - Automatic revalidation
  - Type safety
  - Better performance

### API Routes (Python Script Integration)
- **Location**: `/app/api/`
- **Purpose**: Communication with Python backend only
- **Benefits**:
  - External service integration
  - RESTful endpoints
  - Third-party compatibility

## 📁 File Structure

```
app/
├── actions/                    # Server Actions (Database)
│   ├── grievance-actions.ts   # Grievance CRUD operations
│   └── analytics-actions.ts   # Analytics data operations
├── api/                       # API Routes (Python Integration)
│   ├── ai/
│   │   └── analyze/           # AI analysis endpoints
│   ├── grievances/            # Legacy API (external integrations)
│   │   └── csv/              # CSV upload with Python processing
│   └── analytics/            # Analytics API (calls server action)
└── submit/                   # Updated to use server actions
```

## 🔄 Usage Examples

### 1. Submit Grievance (Server Action)

```tsx
'use client';
import { submitGrievanceAction } from '@/app/actions/grievance-actions';

function SubmitForm() {
  const handleSubmit = async (formData: FormData) => {
    const result = await submitGrievanceAction(formData);
    if (result.success) {
      // Handle success
    }
  };
  
  return (
    <form action={handleSubmit}>
      <textarea name="raw_text" required />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 2. Get Analytics (Server Action)

```tsx
'use client';
import { getAnalyticsAction } from '@/app/actions/analytics-actions';

function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState(null);
  
  useEffect(() => {
    async function loadAnalytics() {
      const result = await getAnalyticsAction();
      if (result.success) {
        setAnalytics(result.data);
      }
    }
    loadAnalytics();
  }, []);
  
  return <div>{/* Render analytics */}</div>;
}
```

### 3. AI Analysis (API Route)

```tsx
// Trigger AI analysis for existing grievance
const analyzeGrievance = async (grievanceId: number, text: string) => {
  const response = await fetch('/api/ai/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grievance_id: grievanceId,
      raw_text: text
    })
  });
  
  return response.json();
};
```

### 4. Check AI Service Status

```tsx
const checkAIStatus = async () => {
  const response = await fetch('/api/ai/analyze');
  const status = await response.json();
  console.log('AI Service:', status.ai_service_status);
};
```

## 🔧 Benefits of This Architecture

### Server Actions Benefits:
- ✅ **Type Safety**: Full TypeScript support
- ✅ **Performance**: Server-side execution
- ✅ **Caching**: Automatic revalidation
- ✅ **Security**: No exposed database credentials
- ✅ **Simplicity**: Direct function calls

### API Routes for Python Only:
- ✅ **Separation of Concerns**: Clear boundaries
- ✅ **External Integrations**: RESTful endpoints
- ✅ **Service Independence**: Python backend can be offline
- ✅ **Scalability**: Each service can scale independently

## 🚀 Migration Guide

### Before (API Route for Database):
```tsx
// ❌ Old way - using API for database
const response = await fetch('/api/grievances', {
  method: 'POST',
  body: JSON.stringify(data)
});
```

### After (Server Action for Database):
```tsx
// ✅ New way - using server action
const result = await submitGrievanceAction(formData);
```

### Python Integration Remains:
```tsx
// ✅ Still use API for Python backend
const analysis = await fetch('/api/ai/analyze', {
  method: 'POST',
  body: JSON.stringify({ raw_text })
});
```

## 📊 Current Implementation Status

### ✅ Completed:
- Server actions for all database operations
- API routes only for Python script interactions
- Updated submit page to use server actions
- Analytics via server actions
- AI analysis via dedicated API routes

### 🔄 Available Endpoints:

#### Server Actions:
- `submitGrievanceAction()` - Store new grievance
- `getAnalyticsAction()` - Get analytics data
- `storeAnalysisResultAction()` - Store AI analysis results
- `storeBatchSummaryAction()` - Store batch summaries

#### API Routes (Python Only):
- `POST /api/ai/analyze` - Trigger AI analysis
- `GET /api/ai/analyze` - Check AI service status
- `POST /api/grievances/csv` - CSV upload with Python processing
- `POST /api/grievances` - External API compatibility

This architecture provides the best of both worlds: fast, type-safe database operations via server actions, and flexible external service integration via API routes.
