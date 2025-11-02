# EV Adoption Forecaster - Installation & Deployment Guide

## 📦 Download & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

#### 1. Download the Project
Download all project files to your local machine or clone the repository.

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Verify Required Files
Ensure these files are present:
- `app.py` - Main Streamlit application
- `forecasting_ev_model.pkl` - Trained ML model
- `preprocessed_ev_data.csv` - Historical EV data
- `ev-car-factory.jpg` - Header image
- `requirements.txt` - Python dependencies

#### 4. Run the Application
```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

---

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

1. **Create a GitHub Repository**
   - Go to [GitHub](https://github.com) and create a new repository
   - Upload all project files to the repository

2. **Deploy to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Click "Deploy"
   - Your app will be live at: `https://[your-app-name].streamlit.app`

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-ev-forecaster-app
   ```

3. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Option 3: AWS EC2

1. **Launch EC2 Instance** (Ubuntu 20.04 or later)
2. **SSH into Instance**
3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements.txt
   ```
4. **Run with Screen**
   ```bash
   screen -S streamlit
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   ```
5. **Configure Security Group** to allow port 8501

### Option 4: Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . /app
   RUN pip install -r requirements.txt
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build & Run**
   ```bash
   docker build -t ev-forecaster .
   docker run -p 8501:8501 ev-forecaster
   ```

---

## 🔧 Configuration

### Customizing the App

**Change Forecast Horizon** (default: 36 months)
```python
# In app.py, line ~70
forecast_horizon = 36  # Change to desired months
```

**Modify Styling**
```python
# In app.py, lines ~15-25
# Edit the CSS in st.markdown() section
```

**Update County List**
The app automatically reads counties from `preprocessed_ev_data.csv`

---

## 📊 Data Requirements

Your CSV file should contain:
- `Date` - Date column (YYYY-MM-DD format)
- `County` - County name
- `Electric Vehicle (EV) Total` - Monthly EV registrations
- `county_encoded` - Encoded county identifier
- `months_since_start` - Months since data collection started

---

## 🐛 Troubleshooting

### Issue: Module not found
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Model file not loading
Ensure `forecasting_ev_model.pkl` is in the same directory as `app.py`

### Issue: Port already in use
```bash
streamlit run app.py --server.port=8502
```

### Issue: Image not displaying
Verify `ev-car-factory.jpg` exists in the project root

---

## 📱 Access Your App

### Local Access
- **URL**: `http://localhost:8501`
- **Network Access**: `http://[your-ip]:8501`

### Public Access (after deployment)
- **Streamlit Cloud**: `https://[your-app-name].streamlit.app`
- **Heroku**: `https://[your-app-name].herokuapp.com`
- **Custom Domain**: Configure DNS to point to your deployment

---

## 🔐 Security Notes

- For production, use environment variables for sensitive data
- Enable HTTPS for public deployments
- Consider adding authentication for restricted access

---

## 📞 Support

For issues or questions:
- Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Review error logs in terminal
- Ensure all dependencies are correctly installed

---

**Prepared for AICTE Internship Cycle 2 by S4F**
