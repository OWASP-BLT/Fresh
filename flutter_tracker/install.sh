#!/bin/bash

# Flutter Activity Tracker - Installation Script
# This script installs Flutter and all dependencies needed for the flutter_tracker

set -e

echo "=================================="
echo "Flutter Activity Tracker Installer"
echo "=================================="
echo ""

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ This app requires Linux"
    exit 1
fi

echo "✅ Linux detected"

# Check for X11
if [ -z "$DISPLAY" ]; then
    echo "⚠️  Warning: X11 display not found. The app will require a graphical session to run."
    echo "   Make sure you run this in a graphical environment when starting the app."
fi

echo ""
echo "=================================="
echo "Installing System Dependencies"
echo "=================================="
echo ""

# Check if we have sudo access
if ! command -v sudo &> /dev/null; then
    echo "❌ sudo not found. This script requires sudo to install system packages."
    exit 1
fi

# Update package list
echo "Updating package list..."
if ! sudo apt-get update; then
    echo "⚠️  Warning: Failed to update package list. Continuing with existing package information..."
fi

# Install required system libraries
echo ""
echo "Installing required system libraries..."
REQUIRED_PACKAGES=(
    "libx11-dev"
    "libxi-dev"
    "libxtst-dev"
    "build-essential"
    "curl"
    "git"
    "unzip"
    "xz-utils"
    "zip"
    "libglu1-mesa"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    if dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q 'install ok installed'; then
        echo "✅ $package already installed"
    else
        echo "📦 Installing $package..."
        sudo apt-get install -y "$package"
    fi
done

echo ""
echo "✅ All system dependencies installed"

echo ""
echo "=================================="
echo "Installing Flutter SDK"
echo "=================================="
echo ""

# Check if Flutter is already installed
if command -v flutter &> /dev/null; then
    echo "✅ Flutter is already installed: $(flutter --version | head -n1)"
    FLUTTER_INSTALLED=true
else
    echo "Flutter not found. Installing Flutter SDK..."
    FLUTTER_INSTALLED=false
fi

if [ "$FLUTTER_INSTALLED" = false ]; then
    # Determine Flutter installation directory
    FLUTTER_DIR="$HOME/flutter"
    
    if [ -d "$FLUTTER_DIR" ]; then
        echo "⚠️  Flutter directory already exists at $FLUTTER_DIR"
        echo "   Using existing directory..."
    else
        echo "Installing Flutter to $FLUTTER_DIR..."
        
        # Clone Flutter repository (stable branch for production use)
        # Use -b beta or -b dev if you need cutting-edge features
        cd "$HOME"
        if ! git clone https://github.com/flutter/flutter.git -b stable --depth 1; then
            echo "❌ Failed to clone Flutter repository"
            exit 1
        fi
    fi
    
    # Add Flutter to PATH for this session
    export PATH="$PATH:$FLUTTER_DIR/bin"
    
    # Add Flutter to PATH permanently
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        if ! grep -q "export PATH=.*flutter/bin" "$SHELL_RC"; then
            {
                echo ""
                echo "# Flutter SDK"
                echo "export PATH=\"\$PATH:$FLUTTER_DIR/bin\""
            } >> "$SHELL_RC"
            echo "✅ Added Flutter to PATH in $SHELL_RC"
        fi
    fi
    
    echo "✅ Flutter installed at $FLUTTER_DIR"
fi

# Verify Flutter installation
echo ""
echo "Verifying Flutter installation..."
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter command not found in PATH"
    echo "   Please add Flutter to your PATH:"
    echo "   export PATH=\"\$PATH:$HOME/flutter/bin\""
    exit 1
fi

echo "✅ Flutter found: $(flutter --version | head -n1)"

# Run flutter doctor to check for any issues
echo ""
echo "Running Flutter doctor to verify installation..."
echo "(This may take a moment...)"
flutter doctor || echo "⚠️  Some Flutter doctor checks failed, but installation can proceed"

# Enable Linux desktop support
echo ""
echo "Enabling Linux desktop support..."
if ! flutter config --enable-linux-desktop; then
    echo "❌ Failed to enable Linux desktop support"
    exit 1
fi

echo "✅ Linux desktop support enabled"

echo ""
echo "=================================="
echo "Building Native Library"
echo "=================================="
echo ""

# Navigate to flutter_tracker directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Build native library
echo "Building native activity tracker library..."
cd linux

if [ ! -f build.sh ]; then
    echo "❌ build.sh not found in linux directory"
    exit 1
fi

chmod +x build.sh
./build.sh

if [ ! -f libactivity_tracker.so ]; then
    echo "❌ Failed to build libactivity_tracker.so"
    exit 1
fi

echo "✅ Native library built successfully"
cd ..

echo ""
echo "=================================="
echo "Installing Flutter Dependencies"
echo "=================================="
echo ""

# Get Flutter dependencies
echo "Running flutter pub get..."
if ! flutter pub get; then
    echo "❌ Failed to get Flutter dependencies"
    exit 1
fi

echo "✅ Flutter dependencies installed"

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "✅ All dependencies have been installed successfully"
echo ""
echo "To run the Flutter Activity Tracker:"
echo "  cd $(pwd)"
echo "  ./run.sh"
echo ""
echo "Or run the demo:"
echo "  ./demo.sh"
echo ""
echo "Note: If this is a new shell session, you may need to restart your terminal"
echo "      or run: source ~/.bashrc (or ~/.zshrc)"
echo ""
