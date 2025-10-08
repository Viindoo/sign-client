#!/bin/bash

# Viindoo Sign Client - macOS Installation Script
# This script automatically installs Python 3.10 and dependencies for macOS

set -e  # Exit on any error

echo "=== Viindoo Sign Client - macOS Installer ==="
echo "Installing dependencies for macOS..."
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script is designed for macOS only."
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    echo "  - Downloading Homebrew installer..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for current session
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -f "/usr/local/bin/brew" ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
    
    echo "✅ Homebrew installed successfully!"
else
    echo "✅ Homebrew is already installed."
fi

# Check if Python 3.10 is installed
if ! command -v python3.10 &> /dev/null; then
    echo "Installing Python 3.10..."
    echo "  - Installing python@3.10 via Homebrew..."
    brew install python@3.10
    
    # Add Python 3.10 to PATH
    echo "  - Adding Python 3.10 to PATH..."
    echo 'export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
    echo 'export PATH="/usr/local/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
    export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"
    export PATH="/usr/local/opt/python@3.10/bin:$PATH"
    
    echo "✅ Python 3.10 installed successfully!"
else
    echo "✅ Python 3.10 is already installed."
fi

# Install python-tk (tkinter) for GUI support
echo "Installing python-tk (tkinter) for GUI support..."
brew install python-tk@3.10
echo "✅ python-tk installed successfully!"

# Install additional system dependencies that might be needed
echo "Installing additional system dependencies..."
brew install pkg-config
echo "✅ pkg-config installed successfully!"

echo ""
echo "Running Python installer to setup application..."
cd "$(dirname "$0")"
python3.10 macos_installer.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Installation completed successfully! ==="
    echo ""
    echo "You can now run Viindoo Sign Client:"
    echo "  - From Applications folder: 'Viindoo Sign Client'"
    echo "  - Command line: ./bin.sh"
    echo "  - Command line: viin-sign-client"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi

echo "For more information, visit: https://github.com/Viindoo/sign-client"
