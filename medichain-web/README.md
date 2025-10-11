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
│   ├── layout.tsx          # Root layout with Navbar + Footer
│   ├── page.tsx            # Home page (landing)
│   ├── globals.css         # Global styles + animations
│   ├── about/
│   │   └── page.tsx        # About page (vision, hackathon info)
│   ├── architecture/
│   │   └── page.tsx        # Architecture page (system diagram, agents)
│   ├── demo/
│   │   └── page.tsx        # Demo page (Agentverse access)
│   └── docs/
│       └── page.tsx        # Documentation page (guides, FAQs)
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx      # Navigation with mobile menu
│   │   ├── Footer.tsx      # Footer with links
│   │   └── Logo.tsx        # Logo component (3 variants)
│   ├── home/
│   │   ├── HeroSection.tsx # Hero with CTA
│   │   ├── ProblemStatement.tsx # Statistics cards
│   │   ├── FeaturesGrid.tsx # Key features (3x2 grid)
│   │   ├── TechStack.tsx   # Technology logos
│   │   └── CTASection.tsx  # Bottom CTA
│   └── shared/
│       ├── Card.tsx        # Reusable card component
│       ├── Button.tsx      # Button variants
│       ├── Badge.tsx       # Badge component
│       ├── AnimatedSection.tsx # Scroll animations
│       └── StatusIndicator.tsx # Agent status
└── public/
    ├── logo.svg            # Horizontal logo
    ├── logo-icon.svg       # Icon only (favicon)
    └── logo-vertical.svg   # Vertical layout
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

### Multi-Page Pitch Website
- 🏠 **Home** - Hero section, problem statement, features grid, tech stack
- 📖 **About** - Project vision, hackathon info, impact metrics, judging criteria
- 🏗️ **Architecture** - System diagram, agent details (4 agents), MeTTa knowledge graph
- 🎮 **Demo** - Live Agentverse access, example test cases, usage guide
- 📚 **Docs** - ASI integration details, resources, FAQs, GitHub links

### Design & UX
- 🎨 Professional medical-grade design system (blue/green palette)
- ✨ Custom animations (fade-in, slide-up, scale-in) with Intersection Observer
- 🔄 Glassmorphism navbar with scroll effects
- 🖼️ Custom logo design (3 SVG variants)
- 📱 Fully responsive (mobile-first, touch-friendly)
- ♿ Accessible (WCAG 2.1 AA, keyboard navigation, ARIA labels)
- 🚀 SEO optimized (metadata, OpenGraph, Twitter Cards)

## License

MIT
