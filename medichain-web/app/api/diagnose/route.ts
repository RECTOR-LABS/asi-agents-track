import { NextRequest, NextResponse } from 'next/server';

// Get coordinator URL from environment variable
const COORDINATOR_URL = process.env.COORDINATOR_URL || 'http://localhost:8080';

// Timeout for coordinator requests (30 seconds)
const REQUEST_TIMEOUT = 30000;

export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json();
    const { message } = body;

    // Validate input
    if (!message || typeof message !== 'string' || message.trim().length === 0) {
      return NextResponse.json(
        {
          error: 'Invalid input',
          details: 'Message is required and must be a non-empty string',
        },
        { status: 400 }
      );
    }

    // Call coordinator agent with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

    let coordinatorResponse;
    try {
      coordinatorResponse = await fetch(`${COORDINATOR_URL}/api/diagnose`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message.trim() }),
        signal: controller.signal,
      });
    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        return NextResponse.json(
          {
            error: 'Request timeout',
            details: 'The diagnostic system took too long to respond. Please try again.',
          },
          { status: 504 }
        );
      }

      // Network error
      console.error('Coordinator fetch error:', fetchError);
      return NextResponse.json(
        {
          error: 'Service unavailable',
          details: 'Unable to connect to the diagnostic system. The coordinator agent may be offline.',
        },
        { status: 503 }
      );
    }

    clearTimeout(timeoutId);

    // Check response status
    if (!coordinatorResponse.ok) {
      const errorText = await coordinatorResponse.text();
      console.error('Coordinator error response:', coordinatorResponse.status, errorText);

      return NextResponse.json(
        {
          error: 'Diagnostic system error',
          details: `The diagnostic system returned an error (${coordinatorResponse.status})`,
        },
        { status: coordinatorResponse.status }
      );
    }

    // Parse coordinator response
    const data = await coordinatorResponse.json();

    // Return successful response
    return NextResponse.json({
      response: data.response || data.error || 'No response from diagnostic system',
      metadata: {
        timestamp: new Date().toISOString(),
        coordinator_url: COORDINATOR_URL,
      },
    });

  } catch (error: any) {
    console.error('API route error:', error);

    return NextResponse.json(
      {
        error: 'Internal server error',
        details: 'An unexpected error occurred while processing your request',
      },
      { status: 500 }
    );
  }
}

// Handle GET requests (health check)
export async function GET() {
  return NextResponse.json({
    status: 'ok',
    service: 'MediChain AI - Diagnostic API',
    coordinator_url: COORDINATOR_URL,
    timestamp: new Date().toISOString(),
  });
}
