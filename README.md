# LinkedIn Automation Platform

Automated LinkedIn content management and posting system.

## Features
- Scheduled post publishing (every 15 minutes)
- Analytics collection (every 4 hours)
- OAuth 2.0 authentication
- Auto-scaling infrastructure
- Real-time dashboard

## Deployment
Deployed on Jelastic PaaS

## API Endpoints
- `GET /api/health` - Health check
- `GET /api/posts` - List posts
- `POST /api/posts` - Create post
- `GET /api/analytics` - Get analytics
- `GET /dashboard` - Web dashboard
- `GET /oauth/start` - Start OAuth flow
- `GET /oauth/status` - Check auth status
