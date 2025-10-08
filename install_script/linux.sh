#!/bin/bash

# Viindoo Sign Client - Linux Installation Script
# This script automatically installs Python 3.10 and dependencies for Linux

set -e  # Exit on any error

echo "=== Viindoo Sign Client - Linux Installer ==="
echo "Installing dependencies for Linux (Ubuntu/Debian)..."
echo ""

# Check if running on supported Linux distribution
if ! command -v apt &> /dev/null; then
    echo "❌ Error: This script is designed for Ubuntu/Debian systems."
    echo "   For other distributions, please install Python 3.10 manually."
    exit 1
fi

# Check if Python 3.10 is installed
if ! command -v python3.10 &>/dev/null; then
    echo "Installing Python 3.10..."
    echo "  - Updating package list..."
    sudo apt update
    
    echo "  - Installing software-properties-common..."
    sudo apt install software-properties-common -y
    
    echo "  - Adding deadsnakes PPA repository..."
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    
    echo "  - Updating package list again..."
    sudo apt update
    
    echo "  - Installing Python 3.10..."
    sudo apt install python3.10 -y
    
    echo "✅ Python 3.10 installed successfully!"
else
    echo "✅ Python 3.10 is already installed."
fi

# Check if python3.10-venv is installed
if ! dpkg -s python3.10-venv &>/dev/null; then
    echo "Installing Python 3.10 virtual environment support..."
    sudo apt install python3.10-venv -y
    echo "✅ Python 3.10 venv installed successfully!"
else
    echo "✅ Python 3.10 venv is already installed."
fi

# Install python3.10-tk for GUI support
echo "Installing python3.10-tk (tkinter) for GUI support..."
sudo apt-get install python3.10-tk -y
echo "✅ python3.10-tk installed successfully!"

echo ""
echo "Running Python installer to setup application..."
sudo python3 linux_installer.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Installation completed successfully! ==="
    echo ""
    echo "You can now run Viindoo Sign Client:"
    echo "  - From Applications menu (Ubuntu)"
    echo "  - Command line: ./bin.sh"
    echo "  - Direct: python3.10 main.py"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi

echo "For more information, visit: https://github.com/Viindoo/sign-client"
