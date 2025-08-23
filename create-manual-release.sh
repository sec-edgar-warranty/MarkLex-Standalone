#!/bin/bash

# Manual Release Creation Script for MarkLex Desktop
# Use this if GitHub Actions fails

set -e

VERSION=${1:-"v1.0.0"}
echo "🚀 Creating manual release: $VERSION"

# Check if gh CLI is installed and authenticated
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "Install it: brew install gh"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

# Check if we have built files
if [[ ! -f "dist/MarkLex-macOS-arm64.zip" ]]; then
    echo "⚠️  macOS ARM64 build not found. Building now..."
    ./build.sh
    cd dist && zip -r MarkLex-macOS-arm64.zip MarkLex.app && cd ..
fi

# Create release
echo "📦 Creating GitHub release..."

RELEASE_NOTES="# MarkLex Desktop $VERSION

## Professional Marketing Lexicon Creation & Text Analysis Tool

### Download Instructions

Choose the appropriate version for your platform:

- **macOS Apple Silicon (M1/M2/M3)**: Download \`MarkLex-macOS-arm64.zip\` ⭐ *Recommended for newer Macs*
- **Windows**: Download \`MarkLex-Windows-x86_64.zip\` (when available)
- **Linux**: Download \`MarkLex-Linux-x86_64.tar.gz\` (when available)

### Installation

#### macOS
1. Download and extract the ZIP file
2. Open \`MarkLex.app\`
3. If you see a security warning, right-click the app and select \"Open\"

#### Windows
1. Download and extract the ZIP file  
2. Run \`MarkLex.exe\`

#### Linux
1. Extract: \`tar -xzf MarkLex-Linux-x86_64.tar.gz\`
2. Run: \`./MarkLex/MarkLex\`

### Features
- ✨ Intelligent lexicon creation using Word2Vec embeddings
- 📊 Text analysis and classification
- 📁 Multiple file format support (CSV, Excel, TXT)
- 🔬 Research-grade accuracy
- 🖥️ Cross-platform desktop application

### Technical Requirements
- **macOS**: 10.15 (Catalina) or later
- **Windows**: Windows 10/11 (64-bit)
- **Linux**: Ubuntu 18.04+ or equivalent

### Verification
Verify download integrity using SHA256 checksums provided in \`checksums.txt\`.

---

🤖 **Note**: This release includes the macOS version. Additional platforms will be added as they become available.

For documentation and support, visit: https://sec-edgar-warranty.github.io/MarkLex-Standalone"

# Create the release
gh release create "$VERSION" \
    --title "MarkLex Desktop $VERSION" \
    --notes "$RELEASE_NOTES"

# Upload available assets
echo "📤 Uploading release assets..."

if [[ -f "dist/MarkLex-macOS-arm64.zip" ]]; then
    echo "Uploading macOS ARM64 build..."
    gh release upload "$VERSION" "dist/MarkLex-macOS-arm64.zip"
fi

if [[ -f "dist/MarkLex-Windows-x86_64.zip" ]]; then
    echo "Uploading Windows build..."
    gh release upload "$VERSION" "dist/MarkLex-Windows-x86_64.zip"
fi

if [[ -f "dist/MarkLex-Linux-x86_64.tar.gz" ]]; then
    echo "Uploading Linux build..."
    gh release upload "$VERSION" "dist/MarkLex-Linux-x86_64.tar.gz"
fi

if [[ -f "dist/checksums.txt" ]]; then
    echo "Uploading checksums..."
    gh release upload "$VERSION" "dist/checksums.txt"
fi

echo "✅ Release $VERSION created successfully!"
echo "🔗 View at: https://github.com/sec-edgar-warranty/MarkLex-Standalone/releases/tag/$VERSION"