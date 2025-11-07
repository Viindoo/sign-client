#!/bin/bash

# Viindoo Sign Client - Linux Uninstall Script
# This script removes the application and all associated files

set -e  # Exit on any error

echo "=== Viindoo Sign Client - Linux Uninstaller ==="
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

# Remove desktop entry from /usr/share/applications
if [[ -f "/usr/share/applications/viin_sign.desktop" ]]; then
    echo "Removing desktop entry..."
    sudo rm -f "/usr/share/applications/viin_sign.desktop"
    echo "✓ Desktop entry removed"
else
    echo "Desktop entry not found"
fi

# Remove application data directory
DATA_DIR="$HOME/.viin_sign_client_data"
if [[ -d "$DATA_DIR" ]]; then
    echo "Removing application data directory..."
    rm -rf "$DATA_DIR"
    echo "✓ Application data directory removed"
else
    echo "Application data directory not found"
fi

# Remove Python virtual environment
VENV_DIR="$(dirname "$0")/../.venv"
if [[ -d "$VENV_DIR" ]]; then
    echo "Removing Python virtual environment..."
    rm -rf "$VENV_DIR"
    echo "✓ Python virtual environment removed"
else
    echo "Python virtual environment not found"
fi

# Remove any system-wide installations (if installed with sudo)
if [[ -d "/opt/viin_sign_client" ]]; then
    echo "Removing system-wide installation..."
    sudo rm -rf "/opt/viin_sign_client"
    echo "✓ System-wide installation removed"
fi

# Remove any symlinks in /usr/local/bin
if [[ -L "/usr/local/bin/viin-sign-client" ]]; then
    echo "Removing command line symlink..."
    sudo rm -f "/usr/local/bin/viin-sign-client"
    echo "✓ Command line symlink removed"
else
    echo "Command line symlink not found"
fi

# Remove any systemd service files (if created)
SERVICE_FILE="/etc/systemd/system/viin-sign-client.service"
if [[ -f "$SERVICE_FILE" ]]; then
    echo "Stopping and removing systemd service..."
    sudo systemctl stop viin-sign-client 2>/dev/null || true
    sudo systemctl disable viin-sign-client 2>/dev/null || true
    sudo rm -f "$SERVICE_FILE"
    sudo systemctl daemon-reload
    echo "✓ Systemd service removed"
fi

# Remove any cron jobs (if created)
CRON_JOB="viin-sign-client"
if crontab -l 2>/dev/null | grep -q "$CRON_JOB"; then
    echo "Removing cron job..."
    crontab -l 2>/dev/null | grep -v "$CRON_JOB" | crontab -
    echo "✓ Cron job removed"
fi

echo ""
echo "=== Uninstall completed successfully! ==="
echo ""
echo "The following items have been removed:"
echo "- Desktop entry from /usr/share/applications"
echo "- Application data directory"
echo "- Python virtual environment"
echo "- System-wide installation (if any)"
echo "- Command line symlink (if any)"
echo "- Systemd service (if any)"
echo "- Cron job (if any)"
echo ""
echo "Note: Python 3.10 and system packages are kept installed as they might be used by other applications."
echo "If you want to remove them as well, you can run:"
echo "  sudo apt remove python3.10 python3.10-venv python3.10-tk"
echo "  sudo apt autoremove"
echo ""
