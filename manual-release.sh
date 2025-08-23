#!/bin/bash

# Manual Release Script - Create release with existing macOS build
# Use this while GitHub Actions workflows are being debugged

set -e

VERSION=${1:-"v1.0.0"}
echo "🚀 Creating manual release: $VERSION"

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not installed. Install with: brew install gh"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI. Run: gh auth login"
    exit 1
fi

# Check if we have the macOS build
if [[ ! -f "dist/MarkLex-macOS-arm64.zip" ]]; then
    echo "⚠️ macOS ARM64 build not found. Creating from existing app..."
    if [[ -d "dist/MarkLex.app" ]]; then
        cd dist && zip -r MarkLex-macOS-arm64.zip MarkLex.app && cd ..
        echo "✅ Created MarkLex-macOS-arm64.zip from existing app bundle"
    else
        echo "❌ No macOS build found. Run ./build.sh first"
        exit 1
    fi
fi

# Create checksums
echo "📊 Creating checksums..."
cd dist
if [[ -f "checksums.txt" ]]; then rm checksums.txt; fi
for file in *.zip *.tar.gz; do
    if [[ -f "$file" && "$file" != "*.zip" && "$file" != "*.tar.gz" ]]; then
        shasum -a 256 "$file" >> checksums.txt
    fi
done 2>/dev/null
cd ..

# Create release notes
RELEASE_NOTES="# MarkLex Desktop $VERSION

## Professional Marketing Lexicon Creation & Text Analysis

A powerful desktop application for creating marketing lexicons using advanced Word2Vec embeddings and performing sophisticated text analysis.

### ✨ Features

- **Intelligent Lexicon Creation**: Build comprehensive marketing lexicons using Word2Vec models
- **Text Analysis**: Analyze documents and classify content using custom lexicons  
- **Multiple File Formats**: Import/export CSV, Excel, and text files
- **Research-Grade**: Suitable for academic research and professional marketing analysis
- **Cross-Platform**: Native desktop application

### 📥 Downloads

#### macOS
- **Apple Silicon (M1/M2/M3)**: \`MarkLex-macOS-arm64.zip\` ⭐ *Recommended for newer Macs*

**Installation**: Extract ZIP file and open \`MarkLex.app\`. If you see a security warning, right-click and select \"Open\".

#### Windows & Linux
*Additional platform builds will be added in future releases.*

### 🔧 Requirements

- **macOS**: 10.15 (Catalina) or later
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space

### 🚀 Getting Started

1. Download and extract the application
2. Open MarkLex.app (macOS) or MarkLex.exe (Windows) 
3. Follow the built-in setup wizard
4. Visit the [documentation](https://sec-edgar-warranty.github.io/MarkLex-Standalone) for detailed instructions

### 🔐 Verification

Verify your download using SHA256 checksums in \`checksums.txt\`:
\`\`\`bash
shasum -a 256 -c checksums.txt
\`\`\`

### 📊 Technical Details

- Built with PyQt6 for modern, native UI
- Includes pre-configured NLTK data for text processing
- Self-contained executable (no Python installation required)
- Uses advanced Word2Vec embeddings for lexicon creation
- Professional-grade text analysis algorithms

---

🚀 **Initial Release**: This is the first release of MarkLex Desktop. Additional platforms and features will be added in future versions.

For support and documentation: https://sec-edgar-warranty.github.io/MarkLex-Standalone

🤖 Generated with [Claude Code](https://claude.ai/code)"

# Create the release
echo "📦 Creating GitHub release..."
echo "$RELEASE_NOTES" > /tmp/marklex_release_notes.md

gh release create "$VERSION" \
    --title "MarkLex Desktop $VERSION" \
    --notes-file "/tmp/marklex_release_notes.md" \
    --target main

# Upload available assets
echo "📤 Uploading release assets..."

if [[ -f "dist/MarkLex-macOS-arm64.zip" ]]; then
    echo "Uploading macOS ARM64 build..."
    gh release upload "$VERSION" "dist/MarkLex-macOS-arm64.zip" --clobber
fi

if [[ -f "dist/checksums.txt" ]]; then
    echo "Uploading checksums..."
    gh release upload "$VERSION" "dist/checksums.txt" --clobber
fi

# Clean up
rm -f /tmp/marklex_release_notes.md

echo "✅ Release $VERSION created successfully!"
echo "🔗 View at: https://github.com/sec-edgar-warranty/MarkLex-Standalone/releases/tag/$VERSION"
echo ""
echo "📋 Next steps:"
echo "1. Visit the release page to verify everything looks correct"
echo "2. Enable GitHub Pages in repository settings (Settings → Pages → /docs folder)"
echo "3. Add more platform builds in future releases"