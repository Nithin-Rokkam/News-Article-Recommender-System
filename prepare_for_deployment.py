#!/usr/bin/env python3
"""
Script to prepare the News Article Recommender System for Vercel deployment
"""

import os
import sys

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'vercel.json',
        'runtime.txt',
        'templates/index.html',
        'Dataset/result_final.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files found")
        return True

def check_dataset_size():
    """Check dataset file size"""
    dataset_path = 'Dataset/result_final.csv'
    if os.path.exists(dataset_path):
        size_mb = os.path.getsize(dataset_path) / (1024 * 1024)
        print(f"📊 Dataset size: {size_mb:.2f} MB")
        
        if size_mb > 50:
            print("⚠️  Warning: Large dataset may cause deployment issues")
            print("   Consider reducing dataset size for faster deployment")
        return True
    return False

def check_requirements():
    """Check requirements.txt content"""
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read()
            if 'Flask' in content and 'scikit-learn' in content:
                print("✅ Requirements.txt looks good")
                return True
            else:
                print("❌ Requirements.txt may be missing key dependencies")
                return False
    return False

def main():
    """Main function"""
    print("🚀 Preparing News Article Recommender System for Vercel deployment...\n")
    
    # Check all requirements
    files_ok = check_required_files()
    dataset_ok = check_dataset_size()
    requirements_ok = check_requirements()
    
    print("\n" + "="*50)
    
    if all([files_ok, dataset_ok, requirements_ok]):
        print("✅ Project is ready for deployment!")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Go to vercel.com and create a new project")
        print("3. Import your GitHub repository")
        print("4. Deploy!")
        print("\n📖 See deploy.md for detailed instructions")
    else:
        print("❌ Project needs fixes before deployment")
        print("Please address the issues above and run this script again")
    
    print("="*50)

if __name__ == "__main__":
    main() 