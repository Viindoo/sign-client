#!/bin/bash

# Viindoo Sign Client - macOS Uninstall Script
# This script removes the application and all associated files

set -e  # Exit on any error

echo "=== Viindoo Sign Client - macOS Uninstaller ==="
echo "This will remove Viindoo Sign Client and all associated files."
echo ""

# Ask for confirmation
read -p "Are you sure you want to uninstall Viindoo Sign Client? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo "Removing application files..."

# Remove App Bundle from Applications
if [[ -d "/Applications/Viindoo Sign Client.app" ]]; then
    echo "Removing App Bundle from Applications..."
    rm -rf "/Applications/Viindoo Sign Client.app"
    echo "✓ App Bundle removed"
else
    echo "App Bundle not found in Applications"
fi

# Remove LaunchAgent plist
LAUNCH_AGENT_PLIST="$HOME/Library/LaunchAgents/com.viindoo.signclient.plist"
if [[ -f "$LAUNCH_AGENT_PLIST" ]]; then
    echo "Removing LaunchAgent plist..."
    rm -f "$LAUNCH_AGENT_PLIST"
    echo "✓ LaunchAgent plist removed"
else
    echo "LaunchAgent plist not found"
fi

# Remove symlink from /usr/local/bin
if [[ -L "/usr/local/bin/viin-sign-client" ]]; then
    echo "Removing command line symlink..."
    rm -f "/usr/local/bin/viin-sign-client"
    echo "✓ Command line symlink removed"
else
    echo "Command line symlink not found"
fi

# Remove application data directory (optional)
DATA_DIR="$HOME/.viin_sign_client_data"
if [[ -d "$DATA_DIR" ]]; then
    read -p "Remove application data directory ($DATA_DIR)? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$DATA_DIR"
        echo "✓ Application data directory removed"
    else
        echo "Application data directory kept"
    fi
else
    echo "Application data directory not found"
fi

# Remove Python virtual environment (optional)
VENV_DIR="$(dirname "$0")/../.venv"
if [[ -d "$VENV_DIR" ]]; then
    read -p "Remove Python virtual environment ($VENV_DIR)? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_DIR"
        echo "✓ Python virtual environment removed"
    else
        echo "Python virtual environment kept"
    fi
else
    echo "Python virtual environment not found"
fi

echo ""
echo "=== Uninstall completed successfully! ==="
echo ""
echo "The following items have been removed:"
echo "- /Applications/Viindoo Sign Client.app"
echo "- ~/Library/LaunchAgents/com.viindoo.signclient.plist"
echo "- /usr/local/bin/viin-sign-client"
echo ""
echo "Note: Homebrew and Python 3.10 are kept installed as they might be used by other applications."
echo "If you want to remove them as well, you can run:"
echo "  brew uninstall python@3.10"
echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)\""
echo ""
