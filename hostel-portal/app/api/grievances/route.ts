import { NextRequest, NextResponse } from 'next/server';
import { submitGrievanceWithCSVFallbackAction } from '@/app/actions/grievance-actions';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { raw_text, user_info } = body;

    if (!raw_text?.trim()) {
      return NextResponse.json({ 
        error: 'raw_text is required' 
      }, { status: 400 });
    }

    // Use the enhanced server action with CSV fallback
    const result = await submitGrievanceWithCSVFallbackAction(
      raw_text.trim(), 
      user_info
    );
    
    if (!result.success) {
      return NextResponse.json({ 
        error: result.error,
        details: result.details 
      }, { status: result.error?.includes('Database') ? 503 : 400 });
    }

    return NextResponse.json({
      success: true,
      grievanceId: result.grievanceId,
      grievance: {
        id: result.grievanceId,
        text: raw_text.trim(),
        category: result.analysisData?.category || 'uncategorized',
        sentiment: result.analysisData?.sentiment || 'neutral',
        urgency: result.analysisData?.urgency || 'low',
        clean_text: result.analysisData?.clean_text || raw_text.trim(),
        analysis_available: !!result.analysisData,
      },
      message: result.analysisData 
        ? 'Grievance submitted and analyzed successfully' 
        : 'Grievance submitted successfully (analysis will be processed later)',
    });

  } catch (error) {
    console.error('Error processing grievance submission:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// GET endpoint to retrieve grievances (for admin use)
export async function GET(request: NextRequest) {
  try {
    // This could be implemented later for retrieving grievances
    // For now, return a simple response
    return NextResponse.json({
      message: "Grievances API endpoint",
      available_endpoints: {
        POST: "Submit a new grievance with automatic AI analysis",
        GET: "Retrieve grievances (not yet implemented)"
      }
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
