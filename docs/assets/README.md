# Website Assets

This folder contains assets for the MarkLex Desktop website.

## Required Images

To complete the website, add these images:

1. **app-screenshot.png** (800x600px recommended)
   - Screenshot of the main MarkLex Desktop application
   - Should show the lexicon creation interface or welcome screen
   - High quality PNG with clean background

2. **marklex-logo.png** ✅ (Already added from app icon)
   - App logo/icon for the navigation header
   - 40px height recommended for display

3. **favicon.png** ✅ (Already added from app icon)
   - Website favicon
   - 32x32px or 16x16px PNG

## Creating Screenshots

To create app-screenshot.png:

1. Build and run the desktop app:
   ```bash
   ./build.sh
   ./dist/MarkLex.app/Contents/MacOS/MarkLex  # macOS
   ```

2. Take a screenshot of the main interface
3. Crop and resize to approximately 800x600px
4. Save as `app-screenshot.png` in this directory

## Alternative

If you don't have a screenshot yet, you can temporarily use a placeholder or create a mockup showing the app interface layout.