#!/usr/bin/env python3
"""
GitHub Release Creator for MarkLex Desktop
Creates GitHub releases with platform-specific builds
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import argparse

def run_command(cmd):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def get_version():
    """Get version from git tags or default"""
    success, output, _ = run_command("git describe --tags --always")
    if success and output:
        return output
    else:
        return "v1.0.0"

def create_release_notes():
    """Generate release notes"""
    version = get_version()
    
    notes = f"""# MarkLex Desktop {version}

## Professional Marketing Lexicon Creation & Text Analysis

MarkLex Desktop is a powerful PyQt6 application for creating marketing lexicons and performing sophisticated text analysis using Word2Vec embeddings.

### ✨ Features

- **Intelligent Lexicon Creation**: Build comprehensive marketing lexicons using advanced Word2Vec models
- **Text Analysis**: Analyze documents and classify content using your custom lexicons
- **Multiple File Formats**: Import from and export to CSV, Excel, and text files
- **Research-Grade**: Suitable for academic research and professional marketing analysis
- **Cross-Platform**: Available for macOS, Windows, and Linux

### 📥 Download Instructions

1. **macOS (Apple Silicon)**: Download `MarkLex-macOS-arm64.zip`
   - Extract the ZIP file
   - Open `MarkLex.app`
   - If you see a security warning, right-click the app and select "Open"

2. **Windows**: Download `MarkLex-Windows.zip` (when available)
   - Extract the ZIP file
   - Run `MarkLex.exe`

3. **Linux**: Download `MarkLex-Linux.tar.gz` (when available)
   - Extract: `tar -xzf MarkLex-Linux.tar.gz`
   - Run: `./MarkLex/MarkLex`

### 🔧 Technical Requirements

- **macOS**: macOS 10.15 or later (Catalina+)
- **Windows**: Windows 10/11 (x64)
- **Linux**: Ubuntu 18.04+ or equivalent

### 📊 Build Information

- Built with PyQt6 for modern UI
- Includes pre-trained Word2Vec models for immediate use
- Self-contained executable (no Python installation required)
- Digitally signed for security (macOS)

### 🔐 Verification

Download checksums are provided in `checksums.txt`. Verify with:
```bash
shasum -a 256 -c checksums.txt
```

### 🚀 Getting Started

1. Download the appropriate version for your platform
2. Extract and run the application
3. Follow the built-in setup wizard to get started
4. Visit the documentation for detailed usage instructions

### 📝 What's New

- Initial release of MarkLex Desktop
- Complete lexicon creation workflow
- Advanced text analysis capabilities
- Professional-grade Word2Vec integration
- Modern, intuitive user interface

---

**Note**: This is the initial release. Additional platforms and features will be added in future versions.

🤖 Generated with [Claude Code](https://claude.ai/code)
"""
    
    return notes

def main():
    parser = argparse.ArgumentParser(description='Create GitHub release for MarkLex Desktop')
    parser.add_argument('--tag', default=None, help='Release tag (default: auto-detect)')
    parser.add_argument('--draft', action='store_true', help='Create as draft release')
    
    args = parser.parse_args()
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Please run this script from the MarkLex Desktop root directory")
        return 1
    
    # Check if gh CLI is available
    success, _, _ = run_command("gh --version")
    if not success:
        print("❌ GitHub CLI (gh) is not installed")
        print("Install it from: https://cli.github.com/")
        return 1
    
    # Get version tag
    version = args.tag or get_version()
    print(f"📦 Creating release: {version}")
    
    # Generate release notes
    notes = create_release_notes()
    
    # Create the release
    draft_flag = "--draft" if args.draft else ""
    
    # Check if release already exists
    success, _, _ = run_command(f"gh release view {version}")
    if success:
        print(f"⚠️  Release {version} already exists. Updating...")
        
        # Upload assets if they exist
        assets_to_upload = []
        
        if os.path.exists("dist/MarkLex-macOS-arm64.zip"):
            assets_to_upload.append("dist/MarkLex-macOS-arm64.zip")
            
        if os.path.exists("dist/MarkLex-Windows.zip"):
            assets_to_upload.append("dist/MarkLex-Windows.zip")
            
        if os.path.exists("dist/MarkLex-Linux.tar.gz"):
            assets_to_upload.append("dist/MarkLex-Linux.tar.gz")
            
        if os.path.exists("dist/checksums.txt"):
            assets_to_upload.append("dist/checksums.txt")
        
        for asset in assets_to_upload:
            success, _, error = run_command(f"gh release upload {version} {asset}")
            if success:
                print(f"✅ Uploaded: {asset}")
            else:
                print(f"❌ Failed to upload {asset}: {error}")
    
    else:
        # Create new release
        print(f"🚀 Creating new release: {version}")
        
        # Write release notes to temp file
        notes_file = "/tmp/marklex_release_notes.md"
        with open(notes_file, "w") as f:
            f.write(notes)
        
        # Create release command
        assets = []
        if os.path.exists("dist/MarkLex-macOS-arm64.zip"):
            assets.append("dist/MarkLex-macOS-arm64.zip")
        if os.path.exists("dist/MarkLex-Windows.zip"):
            assets.append("dist/MarkLex-Windows.zip")
        if os.path.exists("dist/MarkLex-Linux.tar.gz"):
            assets.append("dist/MarkLex-Linux.tar.gz")
        if os.path.exists("dist/checksums.txt"):
            assets.append("dist/checksums.txt")
        
        asset_flags = " ".join([f'"{asset}"' for asset in assets])
        
        cmd = f'gh release create {version} {asset_flags} --title "MarkLex Desktop {version}" --notes-file "{notes_file}" {draft_flag}'
        
        success, output, error = run_command(cmd)
        
        if success:
            print(f"✅ Release created successfully!")
            print(f"📋 Release URL: {output}")
            
            # Clean up
            os.remove(notes_file)
            
        else:
            print(f"❌ Failed to create release: {error}")
            return 1
    
    print("\n🎉 GitHub release process completed!")
    print("\n📋 Next steps:")
    print("1. Visit the GitHub repository to verify the release")
    print("2. Test the download links")
    print("3. Update the website download links if needed")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())