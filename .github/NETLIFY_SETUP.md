# Netlify CI/CD Setup Guide

This guide explains how to set up automatic Netlify deployment using GitHub Actions.

## Required GitHub Secrets

You need to add the following secrets to your GitHub repository:

### 1. NETLIFY_AUTH_TOKEN
- Go to [Netlify Personal Access Tokens](https://app.netlify.com/user/applications#personal-access-tokens)
- Click "New access token"
- Give it a descriptive name (e.g., "GitHub Actions Deploy")
- Copy the generated token

### 2. NETLIFY_SITE_ID
- Go to your Netlify site dashboard
- Navigate to Site settings → General
- Copy the "Site ID" (or "API ID")

## Adding Secrets to GitHub

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret** for each secret:
   - Name: `NETLIFY_AUTH_TOKEN`, Value: Your Netlify personal access token
   - Name: `NETLIFY_SITE_ID`, Value: Your Netlify site ID

## How the CI/CD Works

### Triggers
- **Push to `docker-deployment` branch**: Deploys to production
- **Pull Request to `docker-deployment` branch**: Creates a deploy preview
- **Path filtering**: Only triggers when `frontend/` or `netlify.toml` files change

### Workflow Steps
1. ✅ Checkout code
2. ✅ Setup Node.js 16 with npm cache
3. ✅ Install dependencies (`npm ci`)
4. ✅ Build React app (`npm run build`)
5. ✅ Deploy to Netlify (production or preview)
6. ✅ Comment on PR with deploy status (for PRs)

### Environment Variables
The workflow uses the `netlify.toml` configuration file for:
- `REACT_APP_BACKEND_URL` - Backend API endpoint
- Build settings and redirects

## Manual Deployment
You can still deploy manually using:
```bash
cd frontend
netlify deploy --prod
```

## Troubleshooting

### Build Fails
- Check if all dependencies are in `package.json`
- Ensure `package-lock.json` is committed
- Verify Node.js version compatibility

### Deployment Fails
- Verify `NETLIFY_AUTH_TOKEN` is valid
- Check `NETLIFY_SITE_ID` matches your site
- Ensure Netlify site exists and is accessible

### Backend Connection Issues
- Update `REACT_APP_BACKEND_URL` in `netlify.toml`
- Ensure backend URL is accessible from external networks
- Check CORS settings on your backend 