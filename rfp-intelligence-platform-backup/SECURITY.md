# 🚨 SECURITY WARNING

## API Keys
- NEVER commit .env.local to git
- NEVER share your API keys publicly
- Regenerate keys if accidentally exposed

## Before Deployment
1. Remove all API keys from code
2. Use environment variables in production
3. Set up proper authentication
4. Enable CORS protection

## Local Development Only
This setup includes API keys for local testing.
DO NOT deploy with these keys included!

## If Keys Are Exposed
1. Immediately regenerate them in OpenAI/Anthropic dashboards
2. Update .env.local with new keys
3. Check git history for any commits with keys
