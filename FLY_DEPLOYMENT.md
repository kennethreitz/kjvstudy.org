# Fly.io Deployment Guide

This document describes how to deploy kjvstudy.org to Fly.io.

## Prerequisites

- [Fly.io CLI](https://fly.io/docs/hands-on/install-flyctl/) installed
- Fly.io account created

## Configuration

The app is configured for optimal performance on Fly.io:

### Memory & CPU
- **Memory**: 2GB (to handle 139MB uncompressed interlinear data in memory)
- **CPUs**: 2 shared CPUs
- **Auto-scaling**: Machines stop when idle, start automatically on requests

### Health Checks
- **Endpoint**: `/health`
- **Interval**: Every 15 seconds
- **Timeout**: 10 seconds
- **Grace period**: 30 seconds for startup

### Data Optimization
- Interlinear Bible data compressed to 13.5 MB (from 139 MB)
- **Cache warming on startup** - data preloaded for fast first requests
- Production logging with error handling
- Configurable via `PRELOAD_INTERLINEAR` environment variable

## Deployment Steps

### Initial Setup
```bash
# Login to Fly.io
fly auth login

# Deploy the app
fly deploy
```

### Viewing Logs
```bash
# Stream logs
fly logs

# View specific number of log lines
fly logs -n 100
```

### Monitoring
```bash
# Check app status
fly status

# View app info
fly info

# Open the app in browser
fly open
```

### Scaling
```bash
# Scale memory if needed
fly scale memory 4096

# Scale CPUs
fly scale count 2
```

## Important Files

- `fly.toml` - Fly.io configuration
- `Dockerfile` - Multi-stage build with uv
- `.dockerignore` - Excludes large uncompressed files
- `kjvstudy_org/interlinear_data.py.gz` - Compressed interlinear data (13.5 MB)
- `kjvstudy_org/interlinear_loader.py` - Lazy loader with error handling

## Performance Notes

### Memory Usage
- Base app: ~200-300 MB
- Interlinear data (loaded): ~139 MB
- Total: ~400-500 MB
- Allocated: 2 GB (comfortable headroom)

### Startup Time
- Docker build: ~30-60 seconds
- **With preload enabled** (default):
  - App startup: ~7-10 seconds (loads data on startup)
  - All requests: <100ms (cache is warm)
- **With preload disabled**:
  - App startup: ~5 seconds
  - First interlinear request: ~2-3 seconds
  - Subsequent requests: <100ms

### Auto-Scaling
- Machines stop after 5 minutes of inactivity
- First request after sleep: ~5-10 seconds (cold start + data load)
- Consider keeping 1 machine always running for production:
  ```bash
  fly scale count 1 --max-per-region 1
  ```

## Configuration Options

### Disable Preload (if needed)
If you want faster startup at the cost of slower first interlinear request:

1. Edit `fly.toml`:
```toml
[env]
PRELOAD_INTERLINEAR = "false"  # Disable cache warming
```

2. Deploy:
```bash
fly deploy
```

**When to disable:**
- Testing/development environments
- If startup time is critical
- If interlinear feature is rarely used

**When to keep enabled (default):**
- Production environments
- When users frequently access interlinear verses
- When you want consistent fast performance

## Troubleshooting

### Data Loading Errors
Check logs for interlinear data loading:
```bash
fly logs | grep -i interlinear
```

Should see:
```
Loading interlinear data from /app/kjvstudy_org/interlinear_data.py.gz...
Successfully loaded 31031 verses
```

### Memory Issues
If OOM errors occur, increase memory:
```bash
fly scale memory 4096
```

### SSL/HTTPS
Fly.io automatically provides SSL certificates. The `force_https = true` setting ensures all HTTP requests redirect to HTTPS.

## URLs

- Production: https://kjvstudy.fly.dev
- Health check: https://kjvstudy.fly.dev/health
- Interlinear Bible: https://kjvstudy.fly.dev/interlinear

## Support

For Fly.io specific issues, see:
- [Fly.io Documentation](https://fly.io/docs/)
- [Fly.io Community](https://community.fly.io/)
