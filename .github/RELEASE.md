# GitHub Actions Release Guide

This repository uses GitHub Actions to automatically build MarkLex Desktop for all supported platforms.

## 🚀 Automated Workflows

### 1. Build Workflow (`.github/workflows/build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`
- Manual trigger via GitHub UI

**What it does:**
- Tests the application on all platforms
- Builds executables for:
  - Linux (x86_64)
  - Windows (x86_64) 
  - macOS Intel (x86_64)
  - macOS Apple Silicon (arm64)
- Uploads build artifacts for download

### 2. Release Workflow (`.github/workflows/release.yml`)

**Triggers:**
- Push a git tag matching `v*.*.*` (e.g., `v1.0.0`)
- Manual trigger with custom version

**What it does:**
- Builds all platform executables
- Generates checksums for verification
- Creates a GitHub release with all assets
- Automatically generates comprehensive release notes

## 📋 How to Create a Release

### Method 1: Git Tags (Recommended)

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

The release workflow will automatically:
1. Build for all platforms (Linux, Windows, macOS Intel, macOS ARM64)
2. Create release packages
3. Generate checksums
4. Create GitHub release with all files

### Method 2: Manual Trigger

1. Go to **Actions** tab in your GitHub repository
2. Click **Release** workflow
3. Click **Run workflow**
4. Enter version (e.g., `v1.0.0`)
5. Click **Run workflow**

## 📦 Release Assets

Each release automatically includes:

- `MarkLex-Linux-x86_64.tar.gz` - Linux executable
- `MarkLex-Windows-x86_64.zip` - Windows executable  
- `MarkLex-macOS-x86_64.zip` - macOS Intel executable
- `MarkLex-macOS-arm64.zip` - macOS Apple Silicon executable
- `checksums.txt` - SHA256 checksums for all files

## 🔧 Platform-Specific Build Details

### Linux (Ubuntu Latest)
- **Runner**: `ubuntu-latest`
- **Spec File**: `MarkLex-Linux.spec`
- **Dependencies**: X11 libraries, OpenGL, audio libraries
- **Output**: Single-file executable in tar.gz

### Windows (Latest)
- **Runner**: `windows-latest` 
- **Spec File**: `MarkLex-Windows.spec`
- **Dependencies**: None (Windows has built-in Qt support)
- **Output**: Single-file executable in ZIP

### macOS Intel
- **Runner**: `macos-latest`
- **Spec File**: `MarkLex.spec`
- **Dependencies**: None (uses system frameworks)
- **Output**: App bundle (.app) in ZIP

### macOS Apple Silicon
- **Runner**: `macos-14` (Apple Silicon)
- **Spec File**: `MarkLex.spec` 
- **Dependencies**: None (uses system frameworks)
- **Output**: App bundle (.app) in ZIP

## 🎯 Build Matrix Strategy

The workflows use GitHub Actions matrix strategy to build efficiently:

```yaml
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        platform: linux
      - os: windows-latest  
        platform: windows
      - os: macos-latest
        platform: macos-intel
      - os: macos-14
        platform: macos-arm
```

This ensures all platforms build in parallel, reducing total build time.

## 🔍 Troubleshooting

### Build Failures

1. **Check the Actions tab** for detailed logs
2. **Common issues:**
   - Missing dependencies in `requirements.txt`
   - Platform-specific import errors
   - PyInstaller spec file issues

### Release Issues

1. **Permission denied**: Ensure repository has proper permissions
2. **Tag already exists**: Delete and recreate the tag if needed:
   ```bash
   git tag -d v1.0.0
   git push --delete origin v1.0.0
   git tag v1.0.0
   git push origin v1.0.0
   ```

## 📈 Monitoring Builds

- **Actions Tab**: View all workflow runs
- **Artifacts**: Download build artifacts from successful runs
- **Releases**: View all published releases with download counts

## 🛠 Customization

### Adding New Platforms

1. Update the matrix in both workflow files
2. Add appropriate PyInstaller spec file
3. Update system dependencies if needed

### Modifying Release Notes

Edit the release notes template in `.github/workflows/release.yml` under the "Generate release notes" step.

### Build Optimization

- **Caching**: The workflows use pip caching for faster builds
- **Parallel builds**: All platforms build simultaneously
- **Artifact compression**: Automatic compression for smaller downloads

## 📊 Build Statistics

Typical build times:
- **Linux**: ~15-20 minutes
- **Windows**: ~10-15 minutes
- **macOS**: ~15-20 minutes each

Total release time: ~25-30 minutes for all platforms.