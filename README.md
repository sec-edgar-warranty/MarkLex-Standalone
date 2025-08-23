# MarkLex Desktop

A standalone desktop application for marketing lexicon creation and text analysis, built with PyQt6 and powered by Word2Vec embeddings.

## Features

- **Lexicon Creation**: Generate semantically similar terms using Word2Vec embeddings
- **Text Analysis**: Analyze documents against business dimensions (Marketing, ESG, Risk, etc.)
- **Standalone**: No Python installation required for end users
- **Cross-platform**: Works on macOS, Windows, and Linux
- **Automatic Downloads**: Embedding models downloaded from GitHub on first run
- **Export Capabilities**: CSV export for further analysis

## Quick Start

### For End Users

1. Download the appropriate installer for your platform
2. Install MarkLex Desktop
3. Launch the application
4. Go to the "Setup" tab to download required models (first time only)
5. Start creating lexicons in the "Lexicon" tab
6. Analyze text in the "Text Analysis" tab

### For Developers

#### Building from Source

1. **Clone and setup:**
   ```bash
   cd marklex-desktop
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run in development mode:**
   ```bash
   python main.py
   ```

3. **Build standalone executable:**
   ```bash
   ./build.sh
   ```

## Architecture

```
marklex-desktop/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── build_spec.py             # PyInstaller configuration
├── build.sh                  # Build script
└── src/
    ├── main_window.py         # Main application window
    ├── models/
    │   ├── embedding_manager.py    # Word2Vec model management
    │   ├── text_processor.py       # Text processing utilities
    │   └── lexicon_manager.py      # Lexicon data management
    ├── widgets/
    │   ├── welcome_widget.py       # Welcome/intro tab
    │   ├── setup_widget.py         # Model download interface
    │   ├── lexicon_widget.py       # Lexicon creation interface
    │   └── analysis_widget.py      # Text analysis interface
    └── utils/
        └── app_dirs.py             # Cross-platform directory management
```

## Key Components

### Embedding Manager
- Downloads Word2Vec models from GitHub repository
- Manages unigram and bigram models
- Handles model caching and loading

### Text Processor
- NLTK-based text preprocessing
- N-gram generation (1-3 grams)
- Sentence-level analysis

### Cross-Platform Support
- **macOS**: App bundle with proper permissions and notarization support
- **Windows**: Standalone executable with all dependencies
- **Linux**: Portable executable with bundled libraries

## Building for Distribution

### macOS
```bash
# Build app bundle
./build.sh

# Create DMG (requires create-dmg)
create-dmg --volname "MarkLex" --window-pos 200 120 --window-size 600 300 \
  --icon-size 100 --icon "MarkLex.app" 175 120 --hide-extension "MarkLex.app" \
  --app-drop-link 425 120 "MarkLex.dmg" "dist/"

# Sign for distribution (requires Apple Developer ID)
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" "dist/MarkLex.app"
```

### Windows
```bash
# Build executable
./build.sh

# Create installer with NSIS or Inno Setup
# Example with Inno Setup:
iscc marklex-installer.iss
```

### Linux
```bash
# Build executable  
./build.sh

# Create AppImage (requires linuxdeploy)
linuxdeploy --appdir MarkLex.AppDir --executable dist/MarkLex/MarkLex --desktop-file MarkLex.desktop --icon-file assets/icon.png --output appimage

# Or create DEB package
fpm -s dir -t deb -n marklex -v 1.0.0 --description "Marketing Lexicon Creation Tool" dist/MarkLex/=/opt/marklex/
```

## Data Storage

MarkLex stores data in platform-appropriate locations:

- **macOS**: `~/Library/Application Support/MarkLex/`
- **Windows**: `%APPDATA%/MarkLex/`
- **Linux**: `~/.local/share/MarkLex/`

### Directory Structure
```
MarkLex/
├── embeddings/               # Word2Vec model files
│   ├── embeddings_8          # Unigram model
│   ├── embeddings_8.*.npy    # Model weights
│   └── embeddings_bi_grams   # Bigram model
└── Lexicon List.xlsx         # Default lexicon data
```

## Dependencies

### Runtime (bundled with executable)
- Python 3.8+
- PyQt6
- pandas, numpy, scipy
- gensim (Word2Vec)
- nltk
- requests (for downloads)

### Development Only
- PyInstaller (for building)
- Additional build tools per platform

## Privacy & Security

- **Network Access**: Required only for initial model download
- **Data Storage**: All data stored locally on user's machine
- **No Telemetry**: Application does not collect or transmit usage data
- **macOS Security**: App bundle properly signed and notarized for Gatekeeper

## Troubleshooting

### Common Issues

1. **"App can't be opened" (macOS)**
   - Right-click → "Open" to bypass Gatekeeper
   - Or use: `xattr -cr /path/to/MarkLex.app`

2. **Missing models error**
   - Go to Setup tab and re-download models
   - Check internet connection

3. **Slow startup**
   - Normal on first run (model loading)
   - Subsequent runs should be faster

4. **Memory issues**
   - Models require ~2GB RAM
   - Close other applications if needed

## Development

### Adding Features

1. Create new widget in `src/widgets/`
2. Add to main window tabs
3. Update requirements if needed
4. Test cross-platform compatibility
5. Update build configuration

### Testing

- Test on clean systems without Python
- Verify all features work offline (except download)
- Check memory usage with large documents
- Test export functionality

## License

This project uses the same license as the original MarkLex repository.

## Support

For issues and feature requests, please use the GitHub issue tracker.