#!/bin/bash

# Cross-platform build script for MarkLex Desktop
# Builds Windows and Linux executables on macOS using Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔨 MarkLex Cross-Platform Builder${NC}"
echo "=================================="

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is required but not installed.${NC}"
    echo "Please install Docker Desktop from https://docker.com"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running.${NC}"
    echo "Please start Docker Desktop"
    exit 1
fi

# Create dist directory
mkdir -p dist

# Build for Windows
echo -e "${YELLOW}🪟 Building Windows executable...${NC}"
docker run --rm -v "$(pwd)":/src -w /src \
  cdrx/pyinstaller-windows:python3.10 \
  "pip install -r requirements.txt && pyinstaller --clean --onedir --windowed --icon=assets/MarkLex-icon.png --add-data 'src:src' --hidden-import=src.main_window --hidden-import=src.widgets.welcome_widget --hidden-import=src.widgets.setup_widget --hidden-import=src.widgets.lexicon_widget --hidden-import=src.widgets.analysis_widget --hidden-import=src.models.embedding_manager --hidden-import=src.models.text_processor --hidden-import=src.models.lexicon_manager --hidden-import=src.utils.app_dirs --hidden-import=src.styles.modern_style --name=MarkLex-Windows main.py"

# Move Windows build to final location
if [ -d "dist/MarkLex-Windows" ]; then
    echo -e "${GREEN}✅ Windows build completed${NC}"
    win_size=$(du -sh dist/MarkLex-Windows | cut -f1)
    echo -e "${BLUE}📏 Windows build size: $win_size${NC}"
else
    echo -e "${RED}❌ Windows build failed${NC}"
fi

# Build for Linux
echo -e "${YELLOW}🐧 Building Linux executable...${NC}"
docker run --rm -v "$(pwd)":/src -w /src \
  cdrx/pyinstaller-linux:python3.10 \
  "pip install -r requirements.txt && pyinstaller --clean --onedir --windowed --add-data 'src:src' --hidden-import=src.main_window --hidden-import=src.widgets.welcome_widget --hidden-import=src.widgets.setup_widget --hidden-import=src.widgets.lexicon_widget --hidden-import=src.widgets.analysis_widget --hidden-import=src.models.embedding_manager --hidden-import=src.models.text_processor --hidden-import=src.models.lexicon_manager --hidden-import=src.utils.app_dirs --hidden-import=src.styles.modern_style --name=MarkLex-Linux main.py"

# Move Linux build to final location
if [ -d "dist/MarkLex-Linux" ]; then
    echo -e "${GREEN}✅ Linux build completed${NC}"
    linux_size=$(du -sh dist/MarkLex-Linux | cut -f1)
    echo -e "${BLUE}📏 Linux build size: $linux_size${NC}"
else
    echo -e "${RED}❌ Linux build failed${NC}"
fi

# Build macOS version locally
echo -e "${YELLOW}🍎 Building macOS executable...${NC}"

# Ensure virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

# Clean and build
rm -rf build/MarkLex-macOS dist/MarkLex-macOS*
pyinstaller --clean --onedir --windowed --icon=assets/MarkLex-icon.icns \
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
  --name=MarkLex-macOS main.py

if [ -d "dist/MarkLex-macOS" ]; then
    echo -e "${GREEN}✅ macOS build completed${NC}"
    mac_size=$(du -sh dist/MarkLex-macOS | cut -f1)
    echo -e "${BLUE}📏 macOS build size: $mac_size${NC}"
else
    echo -e "${RED}❌ macOS build failed${NC}"
fi

echo
echo -e "${GREEN}🎉 Cross-platform build complete!${NC}"
echo -e "${BLUE}📦 Build artifacts:${NC}"
ls -la dist/MarkLex-*/ 2>/dev/null || echo "No builds found"

echo
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Test each executable on respective platforms"
echo "2. Create archives: zip dist/MarkLex-Windows && tar -czf MarkLex-Linux.tar.gz dist/MarkLex-Linux && zip -r MarkLex-macOS.zip dist/MarkLex-macOS"
echo "3. Upload to GitHub releases"