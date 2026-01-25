# 🐳 Docker Guide - Cricket Analytics

## Quick Start with Docker

**Fully automated end-to-end pipeline - no Python setup, no manual data download needed!**

### Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)

---

## 🚀 One-Command E2E Launch

```bash
# Build and start the complete pipeline
docker-compose up --build

# Then open: http://localhost:8501
```

**This single command automatically:**
1. ✅ Downloads cricket data from Cricsheet.org (if not already present)
2. ✅ Processes all matches and generates statistics
3. ✅ Validates outputs
4. ✅ Launches interactive dashboard

**No manual intervention required!** True end-to-end automation.

**First run:** ~3-5 minutes (downloading data)
**Subsequent runs:** ~10 seconds (data already exists)

👉 **See [E2E_GUIDE.md](E2E_GUIDE.md) for complete E2E pipeline details**

---

## 📋 Available Services

### 1. **Interactive Dashboard** (Default)

```bash
docker-compose up dashboard
```

**Access at:** http://localhost:8501

**Features:**
- 📊 Overview statistics
- 🏏 Batting analysis with charts
- ⚾ Bowling analysis with visualizations
- 🎯 Match insights
- 🔍 Player comparison tool

---

### 2. **Jupyter Notebooks** (Development Mode)

```bash
docker-compose --profile dev up
```

**Access at:**
- Dashboard: http://localhost:8501
- Jupyter: http://localhost:8888

No token required - just open the URLs!

**Note:** Dashboard still runs the E2E pipeline automatically in dev mode.

---

### 3. **Manual Pipeline Initialization** (Optional)

If you want to run just the initialization without the dashboard:

```bash
docker-compose --profile init up init
```

This will:
- Download data (if needed)
- Process matches
- Validate outputs
- Exit (without launching dashboard)

**Use case:** Pre-downloading data, testing pipeline, troubleshooting

---

## 🎯 E2E Automated Workflow

### Default Behavior (Fully Automated)

```bash
docker-compose up --build
```

**Automatic steps:**
1. ✅ Check if processed data exists
2. ✅ If not, check if raw YAML exists
3. ✅ If not, download from Cricsheet.org (~50MB)
4. ✅ Process all matches → Generate CSV files
5. ✅ Validate all outputs
6. ✅ Launch dashboard on http://localhost:8501

**Smart pipeline:**
- Skips download if data exists
- Skips processing if CSV files exist
- Idempotent (safe to run multiple times)
- Fast subsequent runs (~10 seconds)

### Force Re-download/Re-process

```bash
# Delete processed data to force re-processing
rm -rf data/processed/

# Delete all data to force re-download
rm -rf data/external/ data/processed/

# Then restart
docker-compose up --build
```

---

## 🛠️ Advanced Usage

### Build the Image

```bash
docker build -t cricket-analytics .
```

### Run Specific Commands

```bash
# Run tests
docker run --rm cricket-analytics pytest tests/

# Run specific script
docker run --rm -v $(pwd)/data:/app/data cricket-analytics python scripts/process_all_matches.py

# Open shell
docker run --rm -it cricket-analytics bash
```

### Custom Port

```bash
# Run dashboard on different port
docker run -p 8080:8501 cricket-analytics
```

---

## 📊 Dashboard Features

### Overview Page
- Total matches, deliveries, players
- Key statistics at a glance
- Toss impact analysis

### Batting Analysis
- Top 10 run scorers table
- Interactive bar charts
- Strike rate vs average scatter plot
- Filter by minimum matches played

### Bowling Analysis
- Top 10 wicket takers
- Economy vs average visualization
- Performance charts

### Match Insights
- Toss decision distribution
- Venue analysis
- Win patterns

### Player Comparison
- Compare up to 5 batsmen or bowlers
- Radar charts for multi-metric comparison
- Side-by-side statistics

---

## 🔧 Docker Compose Commands

### Start Services

```bash
# Start dashboard
docker-compose up dashboard

# Start in detached mode (background)
docker-compose up -d dashboard

# Start with Jupyter (dev profile)
docker-compose --profile dev up

# Start all services
docker-compose --profile dev --profile process up
```

### Stop Services

```bash
# Stop all running services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs

```bash
# View dashboard logs
docker-compose logs dashboard

# Follow logs in real-time
docker-compose logs -f dashboard
```

### Rebuild

```bash
# Rebuild after code changes
docker-compose build

# Rebuild and restart
docker-compose up --build
```

---

## 📁 Volume Mounts

The following directories are mounted from your host machine:

- `./data` → `/app/data` - Persists downloaded and processed data
- `./notebooks` → `/app/notebooks` - Jupyter notebooks

This means:
- Data you download is saved on your machine
- Changes to notebooks are saved
- You can access processed data directly

---

## 🌐 Port Mappings

| Service | Container Port | Host Port | URL |
|---------|---------------|-----------|-----|
| Dashboard | 8501 | 8501 | http://localhost:8501 |
| Jupyter | 8888 | 8888 | http://localhost:8888 |

---

## 🐛 Troubleshooting

### "Port already in use"

```bash
# Check what's using the port
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Use a different port
docker run -p 8080:8501 cricket-analytics
```

### "Data not found" in dashboard

```bash
# Make sure you've downloaded and processed data
docker-compose --profile process up processor
```

### Dashboard not updating

```bash
# Rebuild the image
docker-compose build dashboard
docker-compose up dashboard
```

### Permission errors

```bash
# Fix permissions on Linux
sudo chown -R $USER:$USER data/
```

---

## 🚢 Deployment

### Deploy to Cloud

#### Heroku

```bash
# Login to Heroku
heroku login
heroku container:login

# Create app
heroku create cricket-analytics-app

# Build and push
heroku container:push web -a cricket-analytics-app
heroku container:release web -a cricket-analytics-app

# Open
heroku open -a cricket-analytics-app
```

#### Google Cloud Run

```bash
# Build for cloud
gcloud builds submit --tag gcr.io/PROJECT-ID/cricket-analytics

# Deploy
gcloud run deploy cricket-analytics \
  --image gcr.io/PROJECT-ID/cricket-analytics \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### AWS ECS

```bash
# Tag image
docker tag cricket-analytics:latest YOUR_ECR_REPO/cricket-analytics:latest

# Push to ECR
docker push YOUR_ECR_REPO/cricket-analytics:latest
```

---

## 🔒 Security Notes

### For Production Deployment:

1. **Jupyter notebooks** are disabled by default (dev profile only)
2. **Health checks** are configured
3. **No sensitive data** in image (uses volumes)
4. **Minimal base image** (python:3.10-slim)

### Recommendations:

- Use environment variables for sensitive config
- Add authentication for production dashboards
- Use HTTPS in production
- Regularly update base images

---

## 📦 Image Size Optimization

The Dockerfile uses multi-stage builds to keep the image small:

- **Builder stage**: Installs dependencies
- **Runtime stage**: Copies only necessary files

**Typical image size:** ~500MB (including all dependencies)

---

## 🎓 Best Practices

### Development

```bash
# Use docker-compose for local development
docker-compose --profile dev up

# Mount code for live reload (add to docker-compose.yml)
volumes:
  - ./dashboard:/app/dashboard
```

### Testing

```bash
# Run tests in container
docker-compose run --rm dashboard pytest tests/

# With coverage
docker-compose run --rm dashboard pytest tests/ --cov=scripts
```

### Production

```bash
# Use specific version tags
docker build -t cricket-analytics:v1.0.0 .

# Run with restart policy
docker run -d --restart=unless-stopped cricket-analytics
```

---

## 📚 Additional Resources

- **[Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)**
- **[Docker Compose](https://docs.docker.com/compose/)**
- **[Streamlit Docs](https://docs.streamlit.io/)**
- **[Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)**

---

## ✅ Quick Reference

```bash
# Build
docker-compose build

# Start dashboard
docker-compose up dashboard

# Start with Jupyter
docker-compose --profile dev up

# Process data
docker-compose --profile process up processor

# Stop all
docker-compose down

# View logs
docker-compose logs -f dashboard

# Rebuild and restart
docker-compose up --build
```

---

**Questions?** Check the [main README](README.md) or open an issue on GitHub.

**Built with** 🐳 Docker | 📊 Streamlit | 🏏 Cricket Data
