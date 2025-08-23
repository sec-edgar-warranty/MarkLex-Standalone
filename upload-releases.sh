#!/bin/bash

# Upload script for MarkLex Desktop releases
# Creates archives and uploads to GitHub releases

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📤 MarkLex Release Uploader${NC}"
echo "============================="

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is required but not installed.${NC}"
    echo "Install with: brew install gh"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}🔐 Please authenticate with GitHub:${NC}"
    gh auth login
fi

# Get version from user or use current date
read -p "Enter version tag (e.g., v1.0.0) or press Enter for auto-generated: " VERSION
if [ -z "$VERSION" ]; then
    VERSION="v$(date +%Y.%m.%d)"
fi

echo -e "${YELLOW}🏷️  Using version: $VERSION${NC}"

# Check if builds exist
if [ ! -d "dist" ]; then
    echo -e "${RED}❌ No dist directory found. Run ./build-cross-platform.sh first${NC}"
    exit 1
fi

# Create archives directory
mkdir -p releases

echo -e "${YELLOW}📦 Creating archives...${NC}"

# Create Windows archive
if [ -d "dist/MarkLex-Windows" ]; then
    echo "Creating Windows archive..."
    (cd dist && zip -r "../releases/MarkLex-Windows-${VERSION}.zip" MarkLex-Windows/)
    echo -e "${GREEN}✅ Windows archive created${NC}"
else
    echo -e "${YELLOW}⚠️  Windows build not found${NC}"
fi

# Create Linux archive  
if [ -d "dist/MarkLex-Linux" ]; then
    echo "Creating Linux archive..."
    (cd dist && tar -czf "../releases/MarkLex-Linux-${VERSION}.tar.gz" MarkLex-Linux/)
    echo -e "${GREEN}✅ Linux archive created${NC}"
else
    echo -e "${YELLOW}⚠️  Linux build not found${NC}"
fi

# Create macOS archive
if [ -d "dist/MarkLex-macOS" ]; then
    echo "Creating macOS archive..."
    (cd dist && zip -r "../releases/MarkLex-macOS-${VERSION}.zip" MarkLex-macOS/)
    echo -e "${GREEN}✅ macOS archive created${NC}"
else
    echo -e "${YELLOW}⚠️  macOS build not found${NC}"
fi

echo
echo -e "${BLUE}📋 Release archives:${NC}"
ls -la releases/

# Create GitHub release
echo
echo -e "${YELLOW}🚀 Creating GitHub release...${NC}"

# Check if release already exists
if gh release view "$VERSION" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Release $VERSION already exists. Deleting...${NC}"
    gh release delete "$VERSION" --yes
fi

# Create release notes
cat > release_notes.md << EOF
# MarkLex Desktop $VERSION

## What's New
- Cross-platform standalone executables
- All dependencies bundled (no Python installation required)
- Optimized build sizes with proper dependency inclusion

## Downloads
- **Windows**: MarkLex-Windows-${VERSION}.zip
- **macOS**: MarkLex-macOS-${VERSION}.zip  
- **Linux**: MarkLex-Linux-${VERSION}.tar.gz

## Installation
1. Download the archive for your platform
2. Extract the archive
3. Run the MarkLex executable

## Requirements
- No additional software required
- All dependencies included in the executable

---
🤖 Built with PyInstaller and Docker for true cross-platform compatibility
EOF

# Create the release with extended timeout for slow connections
echo -e "${YELLOW}⏱️  Note: Upload may take several minutes on slow connections...${NC}"
GH_REQUEST_TIMEOUT=600 gh release create "$VERSION" \
  --title "MarkLex Desktop $VERSION" \
  --notes-file release_notes.md \
  releases/*

# Clean up
rm release_notes.md

echo
echo -e "${GREEN}🎉 Release $VERSION created successfully!${NC}"
echo -e "${BLUE}🔗 View at: $(gh repo view --web)/releases/tag/$VERSION${NC}"

# Show release info
echo
echo -e "${BLUE}📊 Release summary:${NC}"
gh release view "$VERSION"