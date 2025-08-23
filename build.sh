#!/bin/bash

# Build script for MarkLex Desktop
# Supports macOS, Windows (via WSL/Git Bash), and Linux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔨 Building MarkLex Desktop Application${NC}"
echo "========================================"

# Detect platform
case "$(uname -s)" in
    Darwin*)    PLATFORM="macOS";;
    Linux*)     PLATFORM="Linux";;
    MINGW*)     PLATFORM="Windows";;
    CYGWIN*)    PLATFORM="Windows";;
    *)          PLATFORM="Unknown";;
esac

echo -e "${YELLOW}Platform: $PLATFORM${NC}"

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1-2)
echo -e "${YELLOW}Python: $python_version${NC}"

if [[ "$python_version" < "3.8" ]]; then
    echo -e "${RED}❌ Error: Python 3.8 or higher is required${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${YELLOW}📥 Installing requirements...${NC}"
pip install -r requirements.txt

# Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.spec

# Create assets directory and placeholder icon if needed
mkdir -p assets
if [ ! -f "assets/icon.png" ]; then
    echo -e "${YELLOW}🖼️  Creating placeholder icon...${NC}"
    # Create a simple placeholder icon using ImageMagick if available
    if command -v convert >/dev/null 2>&1; then
        convert -size 256x256 xc:blue -fill white -gravity center -pointsize 72 -annotate +0+0 "ML" assets/icon.png
        
        # Create platform-specific icons
        if [ "$PLATFORM" == "macOS" ]; then
            # Create icns file for macOS
            mkdir -p assets/icon.iconset
            sips -z 16 16 assets/icon.png --out assets/icon.iconset/icon_16x16.png
            sips -z 32 32 assets/icon.png --out assets/icon.iconset/icon_16x16@2x.png
            sips -z 32 32 assets/icon.png --out assets/icon.iconset/icon_32x32.png
            sips -z 64 64 assets/icon.png --out assets/icon.iconset/icon_32x32@2x.png
            sips -z 128 128 assets/icon.png --out assets/icon.iconset/icon_128x128.png
            sips -z 256 256 assets/icon.png --out assets/icon.iconset/icon_128x128@2x.png
            sips -z 256 256 assets/icon.png --out assets/icon.iconset/icon_256x256.png
            sips -z 512 512 assets/icon.png --out assets/icon.iconset/icon_256x256@2x.png
            iconutil -c icns assets/icon.iconset
            rm -rf assets/icon.iconset
        elif [ "$PLATFORM" == "Windows" ]; then
            # Create ico file for Windows (requires ImageMagick)
            convert assets/icon.png -resize 256x256 assets/icon.ico
        fi
    else
        echo -e "${YELLOW}⚠️  ImageMagick not found, using default icon${NC}"
    fi
fi

# Build with PyInstaller
echo -e "${YELLOW}🏗️  Building application...${NC}"
pyinstaller MarkLex.spec

# Check if build was successful
if [ -d "dist/MarkLex" ]; then
    echo -e "${GREEN}✅ Build completed successfully!${NC}"
    echo
    echo -e "${BLUE}📦 Build artifacts:${NC}"
    ls -la dist/
    echo
    
    # Platform-specific instructions
    case $PLATFORM in
        macOS)
            if [ -d "dist/MarkLex.app" ]; then
                echo -e "${GREEN}🍎 macOS App Bundle created: dist/MarkLex.app${NC}"
                echo -e "${YELLOW}💡 To run: open dist/MarkLex.app${NC}"
                echo -e "${YELLOW}💡 To create DMG: Use create-dmg or similar tool${NC}"
            fi
            ;;
        Windows)
            echo -e "${GREEN}🪟 Windows executable created: dist/MarkLex/MarkLex.exe${NC}"
            echo -e "${YELLOW}💡 To run: dist/MarkLex/MarkLex.exe${NC}"
            echo -e "${YELLOW}💡 To create installer: Use NSIS, Inno Setup, or similar${NC}"
            ;;
        Linux)
            echo -e "${GREEN}🐧 Linux executable created: dist/MarkLex/MarkLex${NC}"
            echo -e "${YELLOW}💡 To run: ./dist/MarkLex/MarkLex${NC}"
            echo -e "${YELLOW}💡 To create package: Use fpm, alien, or similar${NC}"
            ;;
    esac
    
    # Calculate build size
    build_size=$(du -sh dist/MarkLex* | cut -f1)
    echo -e "${BLUE}📏 Build size: $build_size${NC}"
    
    echo
    echo -e "${GREEN}🎉 MarkLex Desktop build complete!${NC}"
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "1. Test the application: Run the executable from dist/"
    echo "2. Create installer package for your platform"
    echo "3. Test on clean systems without Python installed"
    echo "4. Sign the application (macOS/Windows) for distribution"
    
else
    echo -e "${RED}❌ Build failed! Check the output above for errors.${NC}"
    exit 1
fi