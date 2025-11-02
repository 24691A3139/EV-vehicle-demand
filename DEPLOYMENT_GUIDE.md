# 🚀 EV Adoption Forecaster - Deployment Guide

## Quick Links to Access Your App

### 🌐 Recommended: Streamlit Cloud (FREE & Easy)

**Live URL Format**: `https://[your-username]-[repo-name]-[app-name].streamlit.app`

#### Step-by-Step Deployment:

1. **Create GitHub Repository**
   - Go to https://github.com/new
   - Name: `ev-adoption-forecaster`
   - Make it Public
   - Click "Create repository"

2. **Upload Your Files**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ev-adoption-forecaster.git
   git push -u origin main
   ```

3. **Deploy to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub account
   - Select:
     - Repository: `ev-adoption-forecaster`
     - Branch: `main`
     - Main file: `app.py`
   - Click "Deploy!"

4. **Your App is Live! 🎉**
   - URL: `https://[your-username]-ev-adoption-forecaster-app.streamlit.app`
   - Share this link with anyone!

---

## 📱 Alternative Deployment Options

### Option 1: Heroku (Free Tier Available)

**Live URL**: `https://your-app-name.herokuapp.com`

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create ev-forecaster-app

# Create setup.sh
echo "mkdir -p ~/.streamlit/
echo \"[server]
headless = true
port = \$PORT
enableCORS = false
\" > ~/.streamlit/config.toml" > setup.sh

# Create Procfile
echo "web: sh setup.sh && streamlit run app.py" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

### Option 2: Render (Free Tier)

**Live URL**: `https://your-app-name.onrender.com`

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ev-forecaster`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Click "Create Web Service"

### Option 3: Railway (Free Tier)

**Live URL**: `https://your-app-name.railway.app`

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Add environment variable:
   - `PORT`: `8501`
6. Railway auto-detects Python and deploys

### Option 4: Google Cloud Run

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Login
gcloud auth login

# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
EOF

# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/ev-forecaster
gcloud run deploy ev-forecaster --image gcr.io/PROJECT_ID/ev-forecaster --platform managed
```

---

## 🖥️ Local Development

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

**Access at**: `http://localhost:8501`

### Run on Local Network

```bash
streamlit run app.py --server.address=0.0.0.0
```

**Access from other devices**: `http://[your-local-ip]:8501`

Find your IP:
- **Linux/Mac**: `ifconfig | grep inet`
- **Windows**: `ipconfig`

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# Build
docker build -t ev-forecaster .

# Run
docker run -p 8501:8501 ev-forecaster
```

### Docker Compose

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    environment:
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
```

Run: `docker-compose up -d`

---

## 🔗 Custom Domain Setup

### For Streamlit Cloud

1. Go to app settings
2. Click "Custom domain"
3. Add your domain: `forecaster.yourdomain.com`
4. Update DNS:
   ```
   Type: CNAME
   Name: forecaster
   Value: [provided-by-streamlit].streamlit.app
   ```

### For Other Platforms

1. **Heroku**:
   ```bash
   heroku domains:add forecaster.yourdomain.com
   ```

2. **Update DNS**:
   ```
   Type: CNAME
   Name: forecaster
   Value: [your-app].herokuapp.com
   ```

---

## 📊 Monitoring & Analytics

### Add Google Analytics

Add to `app.py`:

```python
import streamlit.components.v1 as components

# Google Analytics
ga_code = """
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
"""
components.html(ga_code, height=0)
```

---

## 🔐 Security Best Practices

### Environment Variables

Create `.streamlit/secrets.toml`:

```toml
[secrets]
api_key = "your-secret-key"
database_url = "your-db-url"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

### HTTPS

All major platforms (Streamlit Cloud, Heroku, Render) provide HTTPS automatically.

---

## 🐛 Troubleshooting

### App Won't Start

1. Check logs:
   ```bash
   # Streamlit Cloud: View in dashboard
   # Heroku: heroku logs --tail
   # Local: Check terminal output
   ```

2. Verify all files are present:
   - `app.py`
   - `requirements.txt`
   - `forecasting_ev_model.pkl`
   - `preprocessed_ev_data.csv`
   - `ev-car-factory.jpg`

### Memory Issues

Add to `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### Slow Loading

1. Optimize data loading with caching (already implemented)
2. Reduce forecast horizon if needed
3. Use smaller image files

---

## 📈 Performance Optimization

### Enable Caching

Already implemented in `app.py`:
```python
@st.cache_data
def load_data():
    # ...
```

### Reduce Memory Usage

```python
# Add to app.py
import gc
gc.collect()
```

---

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Trigger Streamlit Cloud Deploy
        run: echo "Streamlit Cloud auto-deploys on push"
```

---

## 📞 Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **Heroku Docs**: https://devcenter.heroku.com
- **Docker Docs**: https://docs.docker.com

---

## ✅ Deployment Checklist

- [ ] All files uploaded to repository
- [ ] `requirements.txt` is complete
- [ ] Model file (`.pkl`) is included
- [ ] Data file (`.csv`) is included
- [ ] Image file is included
- [ ] Platform selected (Streamlit Cloud recommended)
- [ ] App deployed successfully
- [ ] App accessible via URL
- [ ] Tested on mobile device
- [ ] Custom domain configured (optional)
- [ ] Analytics added (optional)

---

**Your app is ready to share with the world! 🌍**

**Prepared for AICTE Internship Cycle 2 by S4F**
