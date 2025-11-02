#!/bin/bash

# EV Adoption Forecaster - Package Creation Script
# This script creates a downloadable ZIP package of your application

echo "🚀 Creating EV Adoption Forecaster Package..."
echo ""

# Package name with timestamp
PACKAGE_NAME="ev-forecaster-$(date +%Y%m%d-%H%M%S).zip"

# Files to include
echo "📦 Packaging files..."

# Create ZIP excluding unnecessary files
zip -r "$PACKAGE_NAME" \
  app.py \
  requirements.txt \
  forecasting_ev_model.pkl \
  preprocessed_ev_data.csv \
  ev-car-factory.jpg \
  config.py \
  README.md \
  INSTALLATION.md \
  DEPLOYMENT_GUIDE.md \
  DOWNLOAD_PACKAGE.md \
  PREVIEW.html \
  models/ \
  utils/ \
  -x "*.git*" \
  -x "*__pycache__*" \
  -x "*.pyc" \
  -x "*.ipynb" \
  -x "*.ipynb_checkpoints*" \
  -x "*.DS_Store" \
  -x "3ae033f50fa345051652.csv" \
  -x "*.log"

echo ""
echo "✅ Package created successfully!"
echo ""
echo "📦 Package name: $PACKAGE_NAME"
echo "📊 Package size: $(du -h "$PACKAGE_NAME" | cut -f1)"
echo ""
echo "🎉 Your app is ready to download and share!"
echo ""
echo "Next steps:"
echo "1. Download: $PACKAGE_NAME"
echo "2. Extract the ZIP file"
echo "3. Run: pip install -r requirements.txt"
echo "4. Start: streamlit run app.py"
echo ""
echo "📖 For deployment instructions, see DEPLOYMENT_GUIDE.md"
echo ""
