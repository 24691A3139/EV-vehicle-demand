#!/usr/bin/env python3
"""
EV Adoption Forecaster - Package Creation Script
Creates a downloadable ZIP package of the application
"""

import os
import zipfile
from datetime import datetime
import sys

def create_package():
    """Create a ZIP package of the application"""
    
    print("🚀 Creating EV Adoption Forecaster Package...")
    print()
    
    # Package name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    package_name = f"ev-forecaster-{timestamp}.zip"
    
    # Files and directories to include
    files_to_include = [
        'app.py',
        'requirements.txt',
        'forecasting_ev_model.pkl',
        'preprocessed_ev_data.csv',
        'ev-car-factory.jpg',
        'config.py',
        'README.md',
        'INSTALLATION.md',
        'DEPLOYMENT_GUIDE.md',
        'DOWNLOAD_PACKAGE.md',
        'PREVIEW.html',
    ]
    
    dirs_to_include = [
        'models',
        'utils',
    ]
    
    # Files to exclude
    exclude_patterns = [
        '.git',
        '__pycache__',
        '.pyc',
        '.ipynb',
        '.ipynb_checkpoints',
        '.DS_Store',
        '3ae033f50fa345051652.csv',
        '.log',
        'EV vehicle demand.ipynb',
        'EV_Adoption_Forecasting (1).ipynb',
    ]
    
    print("📦 Packaging files...")
    
    try:
        with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add individual files
            for file in files_to_include:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"  ✓ Added: {file}")
                else:
                    print(f"  ⚠ Warning: {file} not found")
            
            # Add directories
            for dir_name in dirs_to_include:
                if os.path.exists(dir_name):
                    for root, dirs, files in os.walk(dir_name):
                        # Skip excluded directories
                        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
                        
                        for file in files:
                            # Skip excluded files
                            if not any(pattern in file for pattern in exclude_patterns):
                                file_path = os.path.join(root, file)
                                zipf.write(file_path)
                                print(f"  ✓ Added: {file_path}")
        
        # Get package size
        package_size = os.path.getsize(package_name)
        size_mb = package_size / (1024 * 1024)
        
        print()
        print("✅ Package created successfully!")
        print()
        print(f"📦 Package name: {package_name}")
        print(f"📊 Package size: {size_mb:.2f} MB")
        print()
        print("🎉 Your app is ready to download and share!")
        print()
        print("Next steps:")
        print(f"1. Download: {package_name}")
        print("2. Extract the ZIP file")
        print("3. Run: pip install -r requirements.txt")
        print("4. Start: streamlit run app.py")
        print()
        print("📖 For deployment instructions, see DEPLOYMENT_GUIDE.md")
        print()
        
        return package_name
        
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_package()
