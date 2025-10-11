# MediChain AI - Web Interface

Professional web interface for MediChain AI's multi-agent medical diagnostic system.

## Quick Start

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

Visit: http://localhost:3000

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Deployment:** Vercel

## Project Structure

```
medichain-web/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── globals.css         # Global styles
│   └── api/
│       └── diagnose/
│           └── route.ts    # API route to coordinator
├── components/
│   ├── ChatInterface.tsx   # Chat UI component
│   ├── DiagnosticReport.tsx # Report display
│   ├── LoadingSpinner.tsx  # Loading states
│   └── ErrorMessage.tsx    # Error handling
└── public/
    └── logo.png            # MediChain AI logo
```

## Environment Variables

```bash
COORDINATOR_URL=http://localhost:8080  # Coordinator HTTP endpoint
```

## Development

```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Environment Variables (Vercel)

- `COORDINATOR_URL`: https://medichain-coordinator.onrender.com

## Features

- 🏥 Professional medical interface
- 💬 Real-time chat with AI diagnostic system
- 📊 Structured diagnostic reports
- ⚠️ Color-coded urgency indicators
- 📱 Fully responsive (mobile + desktop)
- ♿ Accessible (ARIA labels, keyboard navigation)

## License

MIT
