#!/usr/bin/env python3
"""
Release Build Script for MarkLex Desktop
Builds platform-specific executables and packages them for distribution.
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
import tarfile
from pathlib import Path
import argparse

# Colors for output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def print_colored(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.NC}")

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print_colored(f"Command failed: {cmd}", Colors.RED)
            print_colored(f"Error: {result.stderr}", Colors.RED)
            return False
        return True
    except Exception as e:
        print_colored(f"Exception running command: {e}", Colors.RED)
        return False

def clean_builds():
    """Clean previous builds"""
    print_colored("🧹 Cleaning previous builds...", Colors.YELLOW)
    dirs_to_clean = ['build', 'dist']
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
            print_colored(f"Removed {d}/", Colors.YELLOW)

def setup_venv():
    """Setup and activate virtual environment"""
    print_colored("📦 Setting up virtual environment...", Colors.YELLOW)
    
    if not os.path.exists('venv'):
        if not run_command(f"{sys.executable} -m venv venv"):
            return False
    
    # Install requirements
    pip_cmd = 'venv/bin/pip' if platform.system() != 'Windows' else 'venv\\Scripts\\pip'
    if not run_command(f"{pip_cmd} install --upgrade pip"):
        return False
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        return False
    
    return True

def build_macos():
    """Build macOS app bundle"""
    print_colored("🍎 Building macOS version...", Colors.BLUE)
    
    pyinstaller_cmd = 'venv/bin/pyinstaller'
    if not run_command(f"{pyinstaller_cmd} MarkLex.spec"):
        return False
        
    # Create DMG (if create-dmg is available)
    if shutil.which('create-dmg'):
        print_colored("📦 Creating DMG package...", Colors.YELLOW)
        dmg_cmd = (
            "create-dmg "
            "--volname 'MarkLex Desktop' "
            "--window-pos 200 120 "
            "--window-size 600 300 "
            "--icon-size 100 "
            "--icon 'MarkLex.app' 175 120 "
            "--hide-extension 'MarkLex.app' "
            "--app-drop-link 425 120 "
            "dist/MarkLex-macOS.dmg "
            "dist/MarkLex.app"
        )
        run_command(dmg_cmd)
    
    # Create zip archive as backup
    print_colored("📦 Creating ZIP archive...", Colors.YELLOW)
    with zipfile.ZipFile('dist/MarkLex-macOS.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('dist/MarkLex.app'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'dist')
                zipf.write(file_path, arcname)
    
    return True

def build_windows():
    """Build Windows executable"""
    print_colored("🪟 Building Windows version...", Colors.BLUE)
    
    pyinstaller_cmd = 'venv/bin/pyinstaller'  # Adjust for cross-compilation or Windows
    if not run_command(f"{pyinstaller_cmd} MarkLex-Windows.spec"):
        return False
    
    # Create zip archive
    print_colored("📦 Creating ZIP archive...", Colors.YELLOW)
    shutil.make_archive('dist/MarkLex-Windows', 'zip', 'dist', 'MarkLex')
    
    return True

def build_linux():
    """Build Linux executable"""
    print_colored("🐧 Building Linux version...", Colors.BLUE)
    
    pyinstaller_cmd = 'venv/bin/pyinstaller'
    if not run_command(f"{pyinstaller_cmd} MarkLex-Linux.spec"):
        return False
    
    # Create tar.gz archive
    print_colored("📦 Creating TAR.GZ archive...", Colors.YELLOW)
    with tarfile.open('dist/MarkLex-Linux.tar.gz', 'w:gz') as tar:
        tar.add('dist/MarkLex', arcname='MarkLex')
    
    return True

def create_checksums():
    """Create checksums for release files"""
    print_colored("🔐 Creating checksums...", Colors.YELLOW)
    
    import hashlib
    
    checksum_file = 'dist/checksums.txt'
    with open(checksum_file, 'w') as f:
        for file_path in Path('dist').glob('MarkLex-*'):
            if file_path.is_file() and file_path.suffix in ['.zip', '.dmg', '.tar.gz']:
                sha256_hash = hashlib.sha256()
                with open(file_path, 'rb') as bf:
                    for chunk in iter(lambda: bf.read(4096), b''):
                        sha256_hash.update(chunk)
                f.write(f"{sha256_hash.hexdigest()}  {file_path.name}\n")
    
    print_colored(f"Checksums written to {checksum_file}", Colors.GREEN)

def main():
    parser = argparse.ArgumentParser(description='Build MarkLex Desktop for multiple platforms')
    parser.add_argument('--platform', choices=['macos', 'windows', 'linux', 'all'], 
                       default='all', help='Platform to build for')
    parser.add_argument('--clean', action='store_true', help='Clean builds first')
    
    args = parser.parse_args()
    
    print_colored("🔨 MarkLex Desktop Release Builder", Colors.BLUE)
    print_colored("=" * 40, Colors.BLUE)
    
    if args.clean:
        clean_builds()
    
    if not setup_venv():
        print_colored("❌ Failed to setup virtual environment", Colors.RED)
        return 1
    
    success = True
    
    if args.platform in ['macos', 'all']:
        if platform.system() == 'Darwin':
            if not build_macos():
                success = False
        else:
            print_colored("⚠️ macOS builds can only be created on macOS", Colors.YELLOW)
    
    if args.platform in ['windows', 'all']:
        print_colored("ℹ️ Windows builds require Windows environment or Wine", Colors.YELLOW)
        print_colored("Use MarkLex-Windows.spec on a Windows machine", Colors.YELLOW)
    
    if args.platform in ['linux', 'all']:
        if platform.system() == 'Linux':
            if not build_linux():
                success = False
        else:
            print_colored("ℹ️ Linux builds work best on Linux systems", Colors.YELLOW)
            print_colored("Use MarkLex-Linux.spec on a Linux machine", Colors.YELLOW)
    
    # Create checksums for any created files
    dist_files = list(Path('dist').glob('MarkLex-*'))
    if dist_files:
        create_checksums()
    
    if success:
        print_colored("✅ Build completed successfully!", Colors.GREEN)
        print_colored("📋 Next steps:", Colors.YELLOW)
        print("1. Test the built applications")
        print("2. Sign the applications (macOS/Windows)")
        print("3. Create GitHub release with the files")
        return 0
    else:
        print_colored("❌ Some builds failed", Colors.RED)
        return 1

if __name__ == '__main__':
    sys.exit(main())