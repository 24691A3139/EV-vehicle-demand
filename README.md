# 🔮 EV Adoption Forecaster

**Electric Vehicle Adoption Forecast Tool for Washington State Counties**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44.1-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📊 Overview

The **EV Adoption Forecaster** is an advanced machine learning application that predicts electric vehicle adoption trends for counties in Washington State. Using historical data and sophisticated forecasting algorithms, it provides 3-year projections to help policymakers, businesses, and researchers understand future EV market dynamics.

### ✨ Key Features

- 📈 **3-Year Forecasting**: Predict EV adoption trends up to 36 months ahead
- 🗺️ **County-Level Analysis**: Detailed insights for each Washington State county
- 📊 **Visual Analytics**: Interactive charts and cumulative trend graphs
- 🔄 **Multi-County Comparison**: Compare up to 3 counties simultaneously
- 🤖 **ML-Powered**: Advanced machine learning algorithms
- 📱 **Responsive Design**: Works seamlessly on all devices

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# 1. Clone or download the repository
git clone [your-repo-url]
cd ev-adoption-forecaster

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 📥 Download & Preview

### 🌐 Preview the App

Open `PREVIEW.html` in your browser to see:
- Application overview and features
- Technology stack
- Installation instructions
- Deployment options

**No installation required to view the preview!**

### 📦 Download Complete Package

1. **Option 1: Use Python Script**
   ```bash
   python create_package.py
   ```

2. **Option 2: Use Shell Script**
   ```bash
   chmod +x create_package.sh
   ./create_package.sh
   ```

3. **Option 3: Manual ZIP**
   - Select all required files
   - Create ZIP archive
   - Share or deploy

See `DOWNLOAD_PACKAGE.md` for detailed instructions.

---

## 🌐 Deployment

### Recommended: Streamlit Cloud (FREE)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click!

**Your app will be live at**: `https://[username]-[repo]-app.streamlit.app`

### Other Options

- **Heroku**: Free tier available
- **Render**: Easy deployment
- **Railway**: Auto-deployment
- **AWS/GCP**: Full control
- **Docker**: Containerized deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions for all platforms.

---

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **Pandas & NumPy**: Data manipulation
- **Scikit-learn**: Machine learning
- **TensorFlow**: Deep learning
- **Matplotlib & Plotly**: Data visualization
- **Joblib**: Model serialization

---

## 📁 Project Structure

```
ev-adoption-forecaster/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── forecasting_ev_model.pkl    # Trained ML model
├── preprocessed_ev_data.csv    # Historical EV data
├── ev-car-factory.jpg          # Header image
├── config.py                   # Configuration settings
├── README.md                   # This file
├── INSTALLATION.md             # Detailed installation guide
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
├── DOWNLOAD_PACKAGE.md         # Download instructions
├── PREVIEW.html                # Static preview page
├── create_package.py           # Package creation script
├── create_package.sh           # Package creation script (bash)
├── models/                     # Model utilities
│   ├── __init__.py
│   ├── analytics.py
│   ├── gamification.py
│   └── scheduler.py
└── utils/                      # Helper utilities
    ├── __init__.py
    ├── database.py
    └── helpers.py
```

---

## 📊 Data Requirements

The application requires a CSV file with the following columns:

- `Date` - Date in YYYY-MM-DD format
- `County` - County name
- `Electric Vehicle (EV) Total` - Monthly EV registrations
- `county_encoded` - Encoded county identifier
- `months_since_start` - Months since data collection started

---

## 🎯 Usage

1. **Select a County**: Choose from the dropdown menu
2. **View Forecast**: See the 3-year prediction graph
3. **Compare Counties**: Select up to 3 counties to compare trends
4. **Analyze Growth**: Review percentage growth predictions

---

## 🔧 Configuration

Edit `config.py` or modify `app.py` to customize:

- Forecast horizon (default: 36 months)
- Visual styling and colors
- Chart configurations
- Data processing parameters

---

## 📖 Documentation

- **INSTALLATION.md**: Complete installation instructions
- **DEPLOYMENT_GUIDE.md**: Step-by-step deployment for multiple platforms
- **DOWNLOAD_PACKAGE.md**: Download and sharing instructions
- **PREVIEW.html**: Interactive preview page

---

## 🐛 Troubleshooting

### Common Issues

**Module not found**
```bash
pip install --upgrade -r requirements.txt
```

**Model file not loading**
- Ensure `forecasting_ev_model.pkl` is in the project root

**Port already in use**
```bash
streamlit run app.py --server.port=8502
```

**Image not displaying**
- Verify `ev-car-factory.jpg` exists in the project root

See `INSTALLATION.md` for more troubleshooting tips.

---

## 🔗 Links

- **Live Demo**: [Deploy to see your link]
- **Documentation**: See included `.md` files
- **Streamlit Docs**: https://docs.streamlit.io
- **Support**: https://discuss.streamlit.io

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **AICTE Internship Cycle 2 by S4F**
- Washington State Department of Licensing for EV data
- Streamlit for the amazing framework
- Open-source community for libraries and tools

---

## 📞 Support

For issues or questions:
1. Check the documentation files
2. Review troubleshooting section
3. Visit Streamlit Community Forum
4. Open an issue on GitHub

---

## 🚀 Get Started Now!

```bash
# Quick start in 3 commands
pip install -r requirements.txt
streamlit run app.py
# Open http://localhost:8501 in your browser
```

**Or deploy to the cloud in minutes!**

See `DEPLOYMENT_GUIDE.md` for one-click deployment options.

---

**Prepared for AICTE Internship Cycle 2 by S4F**

**Happy Forecasting! 🚗⚡**