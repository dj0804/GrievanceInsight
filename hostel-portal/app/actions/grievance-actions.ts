'use server'

import { revalidatePath } from 'next/cache';
import { insertGrievance, insertAnalysisResult } from '@/db/queries';
import { testDatabaseConnection } from '@/db/index';

export interface SubmitGrievanceResult {
  success: boolean;
  grievanceId?: number;
  error?: string;
  details?: string;
}

export async function submitGrievanceAction(formData: FormData): Promise<SubmitGrievanceResult> {
  try {
    // Test database connection first
    const isConnected = await testDatabaseConnection();
    if (!isConnected) {
      return {
        success: false,
        error: 'Database connection failed',
        details: 'Please check your Neon database connection.'
      };
    }

    // Extract form data
    const rawText = formData.get('raw_text') as string;
    const name = formData.get('name') as string;
    const roomNumber = formData.get('roomNumber') as string;
    const email = formData.get('email') as string;

    if (!rawText?.trim()) {
      return {
        success: false,
        error: 'Grievance text is required'
      };
    }

    // Prepare user info
    const userInfo = (name || roomNumber || email) ? {
      name: name || undefined,
      roomNumber: roomNumber || undefined,
      email: email || undefined,
    } : null;

    // Store the grievance in database
    const grievance = await insertGrievance({
      rawText: rawText.trim(),
      userInfo,
      ipAddress: 'server-action', // Server actions don't have access to IP
    });

    // Revalidate paths that might display this data
    revalidatePath('/admin');
    revalidatePath('/api/analytics');

    return {
      success: true,
      grievanceId: grievance.id
    };

  } catch (error) {
    console.error('Error submitting grievance:', error);
    return {
      success: false,
      error: 'Failed to submit grievance',
      details: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

export async function submitGrievanceWithAnalysisAction(
  rawText: string,
  userInfo: any = null
): Promise<SubmitGrievanceResult & { analysisData?: any }> {
  try {
    // Test database connection first
    const isConnected = await testDatabaseConnection();
    if (!isConnected) {
      return {
        success: false,
        error: 'Database connection failed',
        details: 'Please check your Neon database connection.'
      };
    }

    if (!rawText?.trim()) {
      return {
        success: false,
        error: 'Grievance text is required'
      };
    }

    // Store the grievance in database first
    const grievance = await insertGrievance({
      rawText: rawText.trim(),
      userInfo,
      ipAddress: 'api-action',
    });

    // Revalidate paths that might display this data
    revalidatePath('/admin');

    return {
      success: true,
      grievanceId: grievance.id
    };

  } catch (error) {
    console.error('Error submitting grievance with analysis:', error);
    return {
      success: false,
      error: 'Failed to submit grievance',
      details: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

export async function storeAnalysisResultAction(
  grievanceId: number,
  analysisData: {
    category: string;
    sentiment: string;
    urgency: string;
    cleanText: string;
    confidence?: any;
  }
) {
  try {
    const analysis = await insertAnalysisResult({
      grievanceId,
      category: analysisData.category,
      sentiment: analysisData.sentiment,
      urgency: analysisData.urgency,
      cleanText: analysisData.cleanText,
      confidence: analysisData.confidence || null,
    });

    // Revalidate paths that might display this data
    revalidatePath('/admin');

    return { success: true, analysisId: analysis.id };
  } catch (error) {
    console.error('Error storing analysis result:', error);
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}

export async function submitGrievanceWithAutoAnalysisAction(
  rawText: string,
  userInfo: any = null
): Promise<SubmitGrievanceResult & { analysisData?: any }> {
  try {
    // Test database connection first
    const isConnected = await testDatabaseConnection();
    if (!isConnected) {
      return {
        success: false,
        error: 'Database connection failed',
        details: 'Please check your Neon database connection.'
      };
    }

    if (!rawText?.trim()) {
      return {
        success: false,
        error: 'Grievance text is required'
      };
    }

    // Store the grievance in database first
    const grievance = await insertGrievance({
      rawText: rawText.trim(),
      userInfo,
      ipAddress: 'api-action',
    });

    // Attempt to get AI analysis
    let analysisData = null;
    const backendUrl = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';
    
    try {
      const analysisResponse = await fetch(`${backendUrl}/analyze/single`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ raw_text: rawText.trim() }),
      });

      if (analysisResponse.ok) {
        analysisData = await analysisResponse.json();
        
        // Store the analysis result
        if (analysisData) {
          await insertAnalysisResult({
            grievanceId: grievance.id,
            category: analysisData.category || 'uncategorized',
            sentiment: analysisData.sentiment || 'neutral',
            urgency: analysisData.urgency || 'low',
            cleanText: analysisData.clean_text || rawText.trim(),
            confidence: analysisData.confidence || null,
          });
        }
      }
    } catch (analysisError) {
      console.warn('AI analysis service unavailable:', 
        analysisError instanceof Error ? analysisError.message : 'Unknown error');
      // Continue without analysis - grievance is already stored
    }

    // Revalidate paths that might display this data
    revalidatePath('/admin');
    revalidatePath('/api/analytics');

    return {
      success: true,
      grievanceId: grievance.id,
      analysisData: analysisData || null
    };

  } catch (error) {
    console.error('Error submitting grievance with auto analysis:', error);
    return {
      success: false,
      error: 'Failed to submit grievance',
      details: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

export async function submitGrievanceWithCSVFallbackAction(
  rawText: string,
  userInfo: any = null
): Promise<SubmitGrievanceResult & { analysisData?: any }> {
  try {
    // Test database connection first
    const isConnected = await testDatabaseConnection();
    if (!isConnected) {
      return {
        success: false,
        error: 'Database connection failed',
        details: 'Please check your Neon database connection.'
      };
    }

    if (!rawText?.trim()) {
      return {
        success: false,
        error: 'Grievance text is required'
      };
    }

    // Store the grievance in database first
    const grievance = await insertGrievance({
      rawText: rawText.trim(),
      userInfo,
      ipAddress: 'api-action',
    });

    // Attempt to get AI analysis via direct API call first
    let analysisData = null;
    const backendUrl = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';
    
    try {
      const analysisResponse = await fetch(`${backendUrl}/analyze/single`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ raw_text: rawText.trim() }),
      });

      if (analysisResponse.ok) {
        analysisData = await analysisResponse.json();
      } else {
        throw new Error(`Backend returned status: ${analysisResponse.status}`);
      }
    } catch (directError) {
      console.warn('Direct analysis failed, trying CSV fallback:', directError);
      
      // Fallback: Create a temporary CSV and use the CSV analysis endpoint
      try {
        // Create CSV content
        const csvContent = `raw_text\n"${rawText.trim().replace(/"/g, '""')}"`;
        const csvBlob = new Blob([csvContent], { type: 'text/csv' });
        
        // Create FormData for CSV upload
        const formData = new FormData();
        formData.append('file', csvBlob, 'temp_grievance.csv');
        
        const csvAnalysisResponse = await fetch(`${backendUrl}/analyze/csv`, {
          method: 'POST',
          body: formData,
        });

        if (csvAnalysisResponse.ok) {
          const csvAnalysisData = await csvAnalysisResponse.json();
          if (csvAnalysisData.processed_complaints && csvAnalysisData.processed_complaints.length > 0) {
            const complaint = csvAnalysisData.processed_complaints[0];
            analysisData = {
              category: complaint.category,
              sentiment: complaint.sentiment,
              urgency: complaint.urgency,
              clean_text: complaint.clean_text
            };
          }
        }
      } catch (csvError) {
        console.warn('CSV fallback analysis also failed:', csvError);
      }
    }

    // Store analysis result if we got one
    if (analysisData) {
      try {
        await insertAnalysisResult({
          grievanceId: grievance.id,
          category: analysisData.category || 'uncategorized',
          sentiment: analysisData.sentiment || 'neutral',
          urgency: analysisData.urgency || 'low',
          cleanText: analysisData.clean_text || rawText.trim(),
          confidence: analysisData.confidence || null,
        });
      } catch (analysisStoreError) {
        console.error('Failed to store analysis result:', analysisStoreError);
      }
    }

    // Revalidate paths that might display this data
    revalidatePath('/admin');
    revalidatePath('/api/analytics');

    return {
      success: true,
      grievanceId: grievance.id,
      analysisData: analysisData || null
    };

  } catch (error) {
    console.error('Error submitting grievance with CSV fallback:', error);
    return {
      success: false,
      error: 'Failed to submit grievance',
      details: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}
