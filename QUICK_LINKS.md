# 🔗 EV Adoption Forecaster - Quick Access Links

## 📱 Access Your App

### 🌐 Live Deployment URLs

Once deployed, your app will be accessible at one of these URLs:

#### Streamlit Cloud (Recommended - FREE)
```
https://[your-username]-ev-adoption-forecaster-app.streamlit.app
```

**How to get this link:**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Deploy your app
3. Copy the provided URL

---

#### Heroku
```
https://[your-app-name].herokuapp.com
```

**How to get this link:**
```bash
heroku create [your-app-name]
# Your URL will be shown
```

---

#### Render
```
https://[your-app-name].onrender.com
```

**How to get this link:**
1. Deploy on [render.com](https://render.com)
2. Your URL will be provided

---

#### Railway
```
https://[your-app-name].railway.app
```

**How to get this link:**
1. Deploy on [railway.app](https://railway.app)
2. Your URL will be auto-generated

---

### 💻 Local Access

#### Default Local URL
```
http://localhost:8501
```

**Start the app:**
```bash
streamlit run app.py
```

---

#### Network Access (Access from other devices)
```
http://[your-local-ip]:8501
```

**Find your local IP:**
- **Linux/Mac**: `ifconfig | grep inet`
- **Windows**: `ipconfig`

**Start with network access:**
```bash
streamlit run app.py --server.address=0.0.0.0
```

---

## 📥 Download Links

### Preview Page (No Installation Required)
```
file:///[path-to-project]/PREVIEW.html
```

**Open in browser:**
- Double-click `PREVIEW.html`
- Or drag and drop into browser

---

### Documentation Files

| Document | Purpose | Location |
|----------|---------|----------|
| **README.md** | Project overview | Root directory |
| **INSTALLATION.md** | Installation guide | Root directory |
| **DEPLOYMENT_GUIDE.md** | Deployment instructions | Root directory |
| **DOWNLOAD_PACKAGE.md** | Download instructions | Root directory |
| **PREVIEW.html** | Preview page | Root directory |

---

## 🚀 Quick Deploy Links

### One-Click Deploy Platforms

#### Streamlit Cloud
👉 [share.streamlit.io](https://share.streamlit.io)
- **Cost**: FREE
- **Setup Time**: 2 minutes
- **Best For**: Quick deployment

#### Heroku
👉 [heroku.com](https://www.heroku.com)
- **Cost**: Free tier available
- **Setup Time**: 5 minutes
- **Best For**: Production apps

#### Render
👉 [render.com](https://render.com)
- **Cost**: Free tier available
- **Setup Time**: 3 minutes
- **Best For**: Easy deployment

#### Railway
👉 [railway.app](https://railway.app)
- **Cost**: Free tier available
- **Setup Time**: 2 minutes
- **Best For**: Auto-deployment

---

## 📦 Package Creation

### Create Downloadable Package

**Option 1: Python Script**
```bash
python create_package.py
```

**Option 2: Shell Script**
```bash
./create_package.sh
```

**Output**: `ev-forecaster-[timestamp].zip`

---

## 🔧 Useful Commands

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Upgrade dependencies
pip install -r requirements.txt --upgrade
```

### Running the App
```bash
# Standard run
streamlit run app.py

# Custom port
streamlit run app.py --server.port=8502

# Network access
streamlit run app.py --server.address=0.0.0.0

# With specific browser
streamlit run app.py --browser.serverAddress=localhost
```

### Maintenance
```bash
# Clear cache
streamlit cache clear

# Check Streamlit version
streamlit --version

# Check Python version
python --version
```

---

## 📊 Testing URLs

### Local Testing
- **Main App**: http://localhost:8501
- **Health Check**: http://localhost:8501/_stcore/health
- **Metrics**: http://localhost:8501/_stcore/metrics

### After Deployment
- **Main App**: [Your deployment URL]
- **Health Check**: [Your deployment URL]/_stcore/health

---

## 🌐 Share Your App

### Share Options

1. **Direct Link**: Share your deployment URL
2. **QR Code**: Generate QR code for your URL
3. **Embed**: Use iframe to embed in website
4. **Social Media**: Share on Twitter, LinkedIn, etc.

### Generate QR Code

Visit: [qr-code-generator.com](https://www.qr-code-generator.com)
- Enter your app URL
- Download QR code
- Share the image

---

## 📱 Mobile Access

Your app is fully responsive and works on:
- 📱 Smartphones (iOS & Android)
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

**Access from mobile:**
1. Deploy to cloud (Streamlit Cloud recommended)
2. Open URL on mobile browser
3. Add to home screen for app-like experience

---

## 🔐 Custom Domain Setup

### Point Your Domain to App

**For Streamlit Cloud:**
1. Go to app settings
2. Add custom domain
3. Update DNS:
   ```
   Type: CNAME
   Name: forecaster (or subdomain of choice)
   Value: [provided-by-streamlit].streamlit.app
   ```

**For Other Platforms:**
- Follow platform-specific instructions
- Update DNS CNAME record
- Wait for DNS propagation (up to 48 hours)

---

## 📞 Support Links

### Documentation
- **Streamlit Docs**: https://docs.streamlit.io
- **Python Docs**: https://docs.python.org
- **Pandas Docs**: https://pandas.pydata.org/docs

### Community
- **Streamlit Forum**: https://discuss.streamlit.io
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/streamlit
- **GitHub Issues**: [Your repo]/issues

### Tutorials
- **Streamlit Gallery**: https://streamlit.io/gallery
- **YouTube**: Search "Streamlit tutorial"
- **Medium**: Search "Streamlit deployment"

---

## ✅ Quick Checklist

### Before Sharing
- [ ] App runs locally without errors
- [ ] All features work correctly
- [ ] Data loads properly
- [ ] Charts display correctly
- [ ] Tested on mobile device

### For Deployment
- [ ] All files committed to repository
- [ ] requirements.txt is complete
- [ ] Model and data files included
- [ ] Platform selected
- [ ] App deployed successfully
- [ ] URL is accessible
- [ ] Shared with intended users

---

## 🎯 Next Steps

1. **Test Locally**: `streamlit run app.py`
2. **Preview**: Open `PREVIEW.html`
3. **Deploy**: Choose a platform from above
4. **Share**: Send your URL to users!

---

## 📧 Contact & Support

For technical support:
1. Check documentation files
2. Review troubleshooting section in INSTALLATION.md
3. Visit Streamlit Community Forum
4. Search Stack Overflow

---

**Your app is ready to share with the world! 🌍**

**Quick Start:**
```bash
streamlit run app.py
```

**Quick Deploy:**
Visit [share.streamlit.io](https://share.streamlit.io)

---

**Prepared for AICTE Internship Cycle 2 by S4F**
