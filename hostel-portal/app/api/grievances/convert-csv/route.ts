import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { raw_text } = body;

    if (!raw_text?.trim()) {
      return NextResponse.json({ 
        error: 'raw_text is required' 
      }, { status: 400 });
    }

    // Create CSV format from the single input
    const csvContent = `raw_text\n"${raw_text.trim().replace(/"/g, '""')}"`;
    
    // Forward to the existing CSV analysis endpoint
    const csvBlob = new Blob([csvContent], { type: 'text/csv' });
    const formData = new FormData();
    formData.append('file', csvBlob, 'single_grievance.csv');
    
    const csvAnalysisUrl = new URL('/api/grievances/csv', request.url);
    
    try {
      const csvAnalysisResponse = await fetch(csvAnalysisUrl.toString(), {
        method: 'POST',
        body: formData,
      });

      if (!csvAnalysisResponse.ok) {
        throw new Error(`CSV analysis failed with status: ${csvAnalysisResponse.status}`);
      }

      const analysisResult = await csvAnalysisResponse.json();
      
      // Extract the single processed complaint
      if (analysisResult.processed_complaints && analysisResult.processed_complaints.length > 0) {
        const complaint = analysisResult.processed_complaints[0];
        
        return NextResponse.json({
          success: true,
          grievanceId: complaint.id,
          analysisId: complaint.analysis_id,
          analysis: {
            category: complaint.category,
            sentiment: complaint.sentiment,
            urgency: complaint.urgency,
            clean_text: complaint.clean_text,
            original_text: raw_text.trim()
          },
          message: 'Grievance processed successfully via CSV conversion',
          method: 'csv_conversion'
        });
      } else {
        throw new Error('No processed complaints returned from CSV analysis');
      }

    } catch (csvError) {
      console.error('CSV conversion analysis failed:', csvError);
      return NextResponse.json({
        error: 'Analysis service unavailable',
        details: 'Both direct analysis and CSV conversion failed',
        fallback_message: 'Your grievance has been stored but could not be analyzed at this time'
      }, { status: 503 });
    }

  } catch (error) {
    console.error('Error in CSV conversion endpoint:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: "CSV Conversion API",
    description: "Converts single text inputs to CSV format for enhanced analysis",
    endpoints: {
      POST: "Convert and analyze a single grievance using CSV processing pipeline"
    }
  });
}
