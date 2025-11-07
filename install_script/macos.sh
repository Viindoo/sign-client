#!/bin/bash

# Viindoo Sign Client - macOS Installation Script
# This script automatically installs Python 3.10+ (3.10, 3.11, 3.12, 3.13) and dependencies for macOS

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

# Detect Python version (try 3.13, 3.12, 3.11, 3.10)
PYTHON_VERSION=""
PYTHON_EXE=""

for version in 3.13 3.12 3.11 3.10; do
    if command -v python${version} &> /dev/null; then
        PYTHON_VERSION=${version}
        PYTHON_EXE=python${version}
        break
    fi
done

# If no Python found, install the latest available
if [ -z "$PYTHON_EXE" ]; then
    echo "No Python 3.10+ found. Searching for available Python versions..."
    echo "  - Searching for available Python versions in Homebrew..."
    
    # Search for available Python versions and install the newest one
    PYTHON_TO_INSTALL=""
    for version in 3.13 3.12 3.11 3.10; do
        # Check if formula exists in Homebrew
        if brew info python@${version} 2>/dev/null | grep -q "python@${version}:"; then
            PYTHON_TO_INSTALL=${version}
            echo "  - Found Python ${version} in Homebrew"
            break
        fi
    done
    
    if [ -z "$PYTHON_TO_INSTALL" ]; then
        echo "❌ No Python 3.10+ found in Homebrew. Please install Python 3.10+ manually."
        exit 1
    fi
    
    echo "  - Installing Python ${PYTHON_TO_INSTALL} via Homebrew..."
    brew install python@${PYTHON_TO_INSTALL}
    
    PYTHON_VERSION=${PYTHON_TO_INSTALL}
    PYTHON_EXE=python${PYTHON_TO_INSTALL}
    
    # Add Python to PATH
    echo "  - Adding Python ${PYTHON_TO_INSTALL} to PATH..."
    if [[ -f "/opt/homebrew/opt/python@${PYTHON_TO_INSTALL}/bin/python${PYTHON_TO_INSTALL}" ]]; then
        echo "export PATH=\"/opt/homebrew/opt/python@${PYTHON_TO_INSTALL}/bin:\$PATH\"" >> ~/.zshrc
        export PATH="/opt/homebrew/opt/python@${PYTHON_TO_INSTALL}/bin:$PATH"
    elif [[ -f "/usr/local/opt/python@${PYTHON_TO_INSTALL}/bin/python${PYTHON_TO_INSTALL}" ]]; then
        echo "export PATH=\"/usr/local/opt/python@${PYTHON_TO_INSTALL}/bin:\$PATH\"" >> ~/.zshrc
        export PATH="/usr/local/opt/python@${PYTHON_TO_INSTALL}/bin:$PATH"
    fi
    
    echo "✅ Python ${PYTHON_TO_INSTALL} installed successfully!"
else
    echo "✅ Python ${PYTHON_VERSION} is already installed."
fi

# Install python-tk (tkinter) for GUI support
echo "Installing python-tk (tkinter) for GUI support..."
# Try to install tk for detected version
if brew install python-tk@${PYTHON_VERSION} 2>/dev/null; then
    echo "✅ python-tk@${PYTHON_VERSION} installed successfully!"
else
    # Fallback to generic python-tk
    if brew install python-tk 2>/dev/null; then
        echo "✅ python-tk installed successfully!"
    else
        echo "⚠️  python-tk installation failed, but continuing..."
    fi
fi

# Install additional system dependencies that might be needed
echo "Installing additional system dependencies..."
brew install pkg-config
echo "✅ pkg-config installed successfully!"

echo ""
echo "Running Python installer to setup application..."
cd "$(dirname "$0")"
$PYTHON_EXE macos_installer.py

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
