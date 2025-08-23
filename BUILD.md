# MarkLex Desktop Build Guide

This guide explains how to build MarkLex Desktop for different platforms from your Mac.

## Quick Start

### Option 1: macOS Only (No Docker Required)
```bash
./build-local.sh
```
This creates a properly bundled macOS app with all dependencies.

### Option 2: Cross-Platform (Docker Required) 
```bash
./build-cross-platform.sh
```
This creates executables for Windows, Linux, and macOS using Docker containers.

## Prerequisites

### For macOS-only builds:
- macOS with Python 3.8+
- No additional software needed

### For cross-platform builds:
- Docker Desktop installed and running
- GitHub CLI (optional, for uploading)

## Installation Instructions

### Install Docker (for cross-platform builds)
```bash
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker info
```

### Install GitHub CLI (for uploads)
```bash
brew install gh
gh auth login
```

## Build Process Explained

### The Problem with Cross-Compilation
PyInstaller on macOS cannot create true Windows/Linux executables that include all dependencies. Your original GitHub Actions builds were missing key dependencies like pandas, numpy, etc., resulting in small (~30MB) broken executables.

### The Solution
1. **Docker-based builds**: Use official Python Docker containers to create true native executables
2. **Enhanced dependency collection**: Explicitly include all required modules and data files
3. **Proper bundling**: Ensure all libraries are statically linked or bundled

## Build Scripts

### `build-local.sh`
- Builds only for macOS
- Creates a properly bundled .app with all dependencies
- No external dependencies required
- Results in ~300MB+ executable with everything included

### `build-cross-platform.sh` 
- Builds for Windows, Linux, and macOS
- Uses Docker containers for true cross-platform compilation
- Creates properly bundled executables for each platform
- Requires Docker Desktop

### `upload-releases.sh`
- Packages builds into archives
- Creates GitHub releases
- Uploads all platform builds
- Requires GitHub CLI

## Usage

### 1. Build locally (macOS only)
```bash
./build-local.sh
open dist/MarkLex.app  # Test the app
```

### 2. Build cross-platform
```bash
# Ensure Docker is running
docker info

# Build all platforms
./build-cross-platform.sh

# Test builds (if you have VMs)
# Windows: dist/MarkLex-Windows/MarkLex.exe
# Linux: dist/MarkLex-Linux/MarkLex  
# macOS: dist/MarkLex-macOS/MarkLex
```

### 3. Upload to GitHub
```bash
./upload-releases.sh
```

## Troubleshooting

### Docker Issues
```bash
# Check Docker status
docker info

# Start Docker Desktop
open -a Docker

# Pull required images manually
docker pull cdrx/pyinstaller-windows:python3.10
docker pull cdrx/pyinstaller-linux:python3.10
```

### Build Size Issues
Large build sizes (~300MB+) are normal and expected. This includes:
- Python interpreter
- All dependencies (pandas, numpy, scikit-learn, etc.)
- Qt libraries
- NLTK data

Small builds (~30MB) indicate missing dependencies.

### Missing Dependencies
If builds are missing dependencies, check:
1. Are all packages in requirements.txt?
2. Are hidden imports specified in the spec file?
3. Are data files (like NLTK corpora) included?

### Testing Builds
Always test on clean systems without Python installed:
- Use VMs or separate machines
- Verify the app launches without errors
- Check that all features work

## File Structure After Build

```
dist/
├── MarkLex.app/                    # macOS app bundle (local build)
├── MarkLex-macOS/                  # macOS executable (cross-platform)
├── MarkLex-Windows/                # Windows executable 
└── MarkLex-Linux/                  # Linux executable

releases/                           # Created by upload script
├── MarkLex-macOS-vX.X.X.zip
├── MarkLex-Windows-vX.X.X.zip
└── MarkLex-Linux-vX.X.X.tar.gz
```

## GitHub Integration

The upload script automatically:
1. Creates version-tagged archives
2. Generates release notes
3. Uploads to GitHub releases
4. Updates the repository releases page

Your GitHub Pages site will automatically list these releases.

## Next Steps

1. Test the local build: `./build-local.sh && open dist/MarkLex.app`
2. If satisfied, install Docker for cross-platform builds
3. Build and test all platforms: `./build-cross-platform.sh`  
4. Upload to GitHub: `./upload-releases.sh`

The resulting executables will be fully standalone with all dependencies included.