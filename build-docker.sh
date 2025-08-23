#!/bin/bash

# Enhanced cross-platform build script using Docker
# Builds proper executables for Windows, Linux, and macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔨 MarkLex Cross-Platform Builder v2${NC}"
echo "======================================"

# Check Docker
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop${NC}"
    exit 1
fi

# Clean dist directory
rm -rf dist
mkdir -p dist

# Create Dockerfile for Windows build
echo -e "${YELLOW}📝 Creating Windows build environment...${NC}"
cat > Dockerfile.windows << 'EOF'
FROM python:3.10-slim

# Install Wine for Windows cross-compilation
RUN apt-get update && apt-get install -y \
    wine wine64 \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and source
COPY requirements.txt .
COPY main.py .
COPY qt_setup.py .
COPY src/ ./src/
COPY assets/ ./assets/

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pyinstaller

# Build command will be run when container starts
CMD ["pyinstaller", "--onedir", "--windowed", \
     "--name=MarkLex-Windows", \
     "--icon=assets/MarkLex-icon.png", \
     "--add-data=src:src", \
     "--hidden-import=src.main_window", \
     "--hidden-import=src.widgets.welcome_widget", \
     "--hidden-import=src.widgets.setup_widget", \
     "--hidden-import=src.widgets.lexicon_widget", \
     "--hidden-import=src.widgets.analysis_widget", \
     "--hidden-import=src.models.embedding_manager", \
     "--hidden-import=src.models.text_processor", \
     "--hidden-import=src.models.lexicon_manager", \
     "--hidden-import=src.utils.app_dirs", \
     "--hidden-import=src.styles.modern_style", \
     "--hidden-import=pandas._libs.tslibs.timedeltas", \
     "--hidden-import=pandas._libs.tslibs.np_datetime", \
     "--hidden-import=pandas._libs.tslibs.nattype", \
     "--hidden-import=pandas._libs.skiplist", \
     "--hidden-import=numpy.core._methods", \
     "--hidden-import=numpy.lib.format", \
     "--hidden-import=sklearn.utils._cython_blas", \
     "--hidden-import=sklearn.neighbors._typedefs", \
     "--hidden-import=gensim.models.word2vec", \
     "--hidden-import=gensim.models.keyedvectors", \
     "main.py"]
EOF

# Create Dockerfile for Linux build
echo -e "${YELLOW}📝 Creating Linux build environment...${NC}"
cat > Dockerfile.linux << 'EOF'
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and source
COPY requirements.txt .
COPY main.py .
COPY qt_setup.py .
COPY src/ ./src/
COPY assets/ ./assets/

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pyinstaller

# Build command
CMD ["pyinstaller", "--onedir", "--windowed", \
     "--name=MarkLex-Linux", \
     "--add-data=src:src", \
     "--hidden-import=src.main_window", \
     "--hidden-import=src.widgets.welcome_widget", \
     "--hidden-import=src.widgets.setup_widget", \
     "--hidden-import=src.widgets.lexicon_widget", \
     "--hidden-import=src.widgets.analysis_widget", \
     "--hidden-import=src.models.embedding_manager", \
     "--hidden-import=src.models.text_processor", \
     "--hidden-import=src.models.lexicon_manager", \
     "--hidden-import=src.utils.app_dirs", \
     "--hidden-import=src.styles.modern_style", \
     "--hidden-import=pandas._libs.tslibs.timedeltas", \
     "--hidden-import=pandas._libs.tslibs.np_datetime", \
     "--hidden-import=pandas._libs.tslibs.nattype", \
     "--hidden-import=pandas._libs.skiplist", \
     "--hidden-import=numpy.core._methods", \
     "--hidden-import=numpy.lib.format", \
     "--hidden-import=sklearn.utils._cython_blas", \
     "--hidden-import=sklearn.neighbors._typedefs", \
     "--hidden-import=gensim.models.word2vec", \
     "--hidden-import=gensim.models.keyedvectors", \
     "main.py"]
EOF

# Build Linux version
echo -e "${YELLOW}🐧 Building Linux executable with Docker...${NC}"
docker build -f Dockerfile.linux -t marklex-linux-builder .
docker run --rm -v "$(pwd)/dist:/app/dist" marklex-linux-builder

if [ -d "dist/MarkLex-Linux" ]; then
    echo -e "${GREEN}✅ Linux build completed${NC}"
    linux_size=$(du -sh dist/MarkLex-Linux | cut -f1)
    echo -e "${BLUE}📏 Linux build size: $linux_size${NC}"
else
    echo -e "${YELLOW}⚠️  Linux build may have failed${NC}"
fi

# Note: Windows cross-compilation from Mac/Linux is complex
# For now, we'll build macOS locally and Linux via Docker
echo -e "${YELLOW}⚠️  Note: True Windows builds require a Windows host or VM${NC}"
echo -e "${YELLOW}    Consider using GitHub Actions for Windows builds${NC}"

# Build macOS version locally
echo -e "${YELLOW}🍎 Building macOS executable locally...${NC}"

# Setup virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Clean macOS build
rm -rf build/MarkLex-macOS dist/MarkLex-macOS

# Build macOS
pyinstaller --clean --onedir --windowed \
  --name=MarkLex-macOS \
  --icon=assets/MarkLex-icon.icns \
  --add-data 'src:src' \
  --hidden-import=src.main_window \
  --hidden-import=src.widgets.welcome_widget \
  --hidden-import=src.widgets.setup_widget \
  --hidden-import=src.widgets.lexicon_widget \
  --hidden-import=src.widgets.analysis_widget \
  --hidden-import=src.models.embedding_manager \
  --hidden-import=src.models.text_processor \
  --hidden-import=src.models.lexicon_manager \
  --hidden-import=src.utils.app_dirs \
  --hidden-import=src.styles.modern_style \
  --hidden-import=pandas._libs.tslibs.timedeltas \
  --hidden-import=pandas._libs.tslibs.np_datetime \
  --hidden-import=pandas._libs.tslibs.nattype \
  --hidden-import=pandas._libs.skiplist \
  --hidden-import=numpy.core._methods \
  --hidden-import=numpy.lib.format \
  --hidden-import=sklearn.utils._cython_blas \
  --hidden-import=sklearn.neighbors._typedefs \
  --hidden-import=gensim.models.word2vec \
  --hidden-import=gensim.models.keyedvectors \
  main.py

if [ -d "dist/MarkLex-macOS" ]; then
    echo -e "${GREEN}✅ macOS build completed${NC}"
    mac_size=$(du -sh dist/MarkLex-macOS | cut -f1)
    echo -e "${BLUE}📏 macOS build size: $mac_size${NC}"
else
    echo -e "${RED}❌ macOS build failed${NC}"
fi

# Clean up Docker files
rm -f Dockerfile.windows Dockerfile.linux

echo
echo -e "${GREEN}🎉 Build process complete!${NC}"
echo -e "${BLUE}📦 Available builds:${NC}"
ls -la dist/

echo
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Test Linux build on a Linux VM or machine"
echo "2. For Windows builds, use a Windows machine or GitHub Actions"
echo "3. Create archives and upload: ./upload-releases.sh"