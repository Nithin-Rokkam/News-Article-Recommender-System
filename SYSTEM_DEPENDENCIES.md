# System Dependencies Installation Guide

This guide helps you install the required system packages before running `pip install -r requirements.txt` for the News Article Recommender System.

## Required System Packages

The following system packages are needed for the Python dependencies to compile and run properly:

### For Ubuntu/Debian Linux:
```bash
sudo apt update
sudo apt install -y \
    python3-dev \
    python3-pip \
    build-essential \
    gcc \
    g++ \
    curl \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    pkg-config
```

### For CentOS/RHEL/Fedora:
```bash
# For CentOS/RHEL 7/8
sudo yum groupinstall -y "Development Tools"
sudo yum install -y \
    python3-devel \
    python3-pip \
    gcc \
    gcc-c++ \
    curl \
    libffi-devel \
    openssl-devel \
    zlib-devel \
    libjpeg-turbo-devel \
    libpng-devel \
    freetype-devel \
    lcms2-devel \
    libtiff-devel \
    libwebp-devel \
    harfbuzz-devel \
    fribidi-devel \
    pkgconfig

# For Fedora
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y \
    python3-devel \
    python3-pip \
    gcc \
    gcc-c++ \
    curl \
    libffi-devel \
    openssl-devel \
    zlib-devel \
    libjpeg-turbo-devel \
    libpng-devel \
    freetype-devel \
    lcms2-devel \
    libtiff-devel \
    libwebp-devel \
    harfbuzz-devel \
    fribidi-devel \
    pkgconfig
```

### For macOS (using Homebrew):
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install \
    python3 \
    gcc \
    curl \
    pkg-config \
    libffi \
    openssl \
    zlib \
    jpeg \
    libpng \
    freetype \
    libtiff \
    webp \
    harfbuzz \
    fribidi
```

### For Windows:
For Windows, you'll need to install Visual Studio Build Tools:

1. **Install Visual Studio Build Tools:**
   - Download from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
   - Install "C++ build tools" workload
   - Include Windows 10/11 SDK

2. **Install Windows Subsystem for Linux (WSL) - Recommended:**
   ```bash
   # Enable WSL
   wsl --install
   
   # Then follow Ubuntu instructions above
   ```

3. **Alternative: Use Conda/Miniconda:**
   ```bash
   # Install Miniconda
   # Download from: https://docs.conda.io/en/latest/miniconda.html
   
   # Create environment with pre-compiled packages
   conda create -n news-recommender python=3.11
   conda activate news-recommender
   conda install -c conda-forge scikit-learn pandas numpy
   pip install Flask Werkzeug gunicorn
   ```

## Installation Steps

1. **Install system dependencies** using the commands above for your OS
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   ```
4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Troubleshooting

### Common Issues:

1. **"Microsoft Visual C++ 14.0 is required" (Windows):**
   - Install Visual Studio Build Tools as mentioned above

2. **"fatal error: Python.h: No such file or directory":**
   - Install `python3-dev` package (Ubuntu/Debian)
   - Install `python3-devel` package (CentOS/RHEL/Fedora)

3. **"error: command 'gcc' failed":**
   - Install build tools: `build-essential` (Ubuntu/Debian) or "Development Tools" (CentOS/RHEL)

4. **SSL/TLS errors:**
   - Install `libssl-dev` (Ubuntu/Debian) or `openssl-devel` (CentOS/RHEL)

5. **Memory errors during compilation:**
   - Increase swap space or use pre-compiled wheels:
   ```bash
   pip install --only-binary=all -r requirements.txt
   ```

### Using Pre-compiled Wheels (Recommended):
```bash
# Install using pre-compiled packages when possible
pip install --only-binary=all -r requirements.txt

# If that fails, try with specific packages
pip install --only-binary=all scikit-learn pandas numpy
pip install Flask Werkzeug gunicorn
```

## Verification

After installation, verify everything works:
```bash
python -c "import flask, pandas, numpy, sklearn; print('All packages installed successfully!')"
```

## Docker Alternative

If you continue having issues with system dependencies, consider using Docker:
```bash
# Build and run with Docker
docker build -t news-recommender .
docker run -p 5000:5000 news-recommender
```

This approach isolates all dependencies and avoids system-level package conflicts. 