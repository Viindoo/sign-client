#!/bin/bash

# Viindoo Sign Client - Linux Installation Script
# This script automatically installs Python 3.10+ (3.10, 3.11, 3.12, 3.13) and dependencies for Linux

set -e  # Exit on any error

echo "=== Viindoo Sign Client - Linux Installer ==="
echo "Installing dependencies for Linux (Ubuntu/Debian)..."
echo ""

# Check if running on supported Linux distribution
if ! command -v apt &> /dev/null; then
    echo "❌ Error: This script is designed for Ubuntu/Debian systems."
    echo "   For other distributions, please install Python 3.10+ manually."
    exit 1
fi

# Detect Python version (try 3.13, 3.12, 3.11, 3.10)
PYTHON_VERSION=""
PYTHON_EXE=""

for version in 3.13 3.12 3.11 3.10; do
    if command -v python${version} &>/dev/null; then
        PYTHON_VERSION=${version}
        PYTHON_EXE=python${version}
        break
    fi
done

# If no Python found, install the latest available (prefer 3.13, then 3.12, then 3.11, fallback to 3.10)
if [ -z "$PYTHON_EXE" ]; then
    echo "No Python 3.10+ found. Installing Python 3.13..."
    echo "  - Updating package list..."
    sudo apt update
    
    echo "  - Installing software-properties-common..."
    sudo apt install software-properties-common -y
    
    echo "  - Adding deadsnakes PPA repository..."
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    
    echo "  - Updating package list again..."
    sudo apt update
    
    # Search for available Python versions and install the newest one
    echo "  - Searching for available Python versions..."
    PYTHON_TO_INSTALL=""
    for version in 3.13 3.12 3.11 3.10; do
        # Check if package exists and has a candidate version (not "none")
        policy_output=$(apt-cache policy python${version} 2>/dev/null)
        if echo "$policy_output" | grep -q "Candidate:" && ! echo "$policy_output" | grep -q "Candidate: (none)"; then
            PYTHON_TO_INSTALL=${version}
            echo "  - Found Python ${version} in repository"
            break
        fi
    done
    
    if [ -z "$PYTHON_TO_INSTALL" ]; then
        echo "❌ No Python 3.10+ found in repository. Please install Python 3.10+ manually."
        exit 1
    fi
    
    echo "  - Installing Python ${PYTHON_TO_INSTALL}..."
    sudo apt install python${PYTHON_TO_INSTALL} -y
    PYTHON_VERSION=${PYTHON_TO_INSTALL}
    PYTHON_EXE=python${PYTHON_TO_INSTALL}
    echo "✅ Python ${PYTHON_TO_INSTALL} installed successfully!"
else
    echo "✅ Python ${PYTHON_VERSION} is already installed."
fi

# Check if python-venv is installed
if ! dpkg -s python${PYTHON_VERSION}-venv &>/dev/null; then
    echo "Installing Python ${PYTHON_VERSION} virtual environment support..."
    sudo apt install python${PYTHON_VERSION}-venv -y
    echo "✅ Python ${PYTHON_VERSION} venv installed successfully!"
else
    echo "✅ Python ${PYTHON_VERSION} venv is already installed."
fi

# Install python-tk for GUI support
echo "Installing python${PYTHON_VERSION}-tk (tkinter) for GUI support..."
sudo apt-get install python${PYTHON_VERSION}-tk -y
echo "✅ python${PYTHON_VERSION}-tk installed successfully!"

echo ""
echo "Running Python installer to setup application..."
sudo $PYTHON_EXE linux_installer.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Installation completed successfully! ==="
    echo ""
    echo "You can now run Viindoo Sign Client:"
    echo "  - From Applications menu (Ubuntu)"
    echo "  - Command line: ./bin.sh"
    echo "  - Direct: ${PYTHON_EXE} main.py"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi

echo "For more information, visit: https://github.com/Viindoo/sign-client"
