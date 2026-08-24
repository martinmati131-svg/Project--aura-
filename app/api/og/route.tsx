import { ImageResponse } from '@vercel/og';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const title = searchParams.get('title') || 'Project Aura Blog';

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          backgroundColor: '#09090b',
          color: '#ffffff',
          padding: '80px',
          fontFamily: 'sans-serif',
        }}
      >
        <div style={{ fontSize: 28, color: '#a1a1aa', marginBottom: 20 }}>
          PROJECT AURA
        </div>
        <div style={{ fontSize: 60, fontWeight: 'bold', lineHeight: 1.2 }}>
          {title}
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
