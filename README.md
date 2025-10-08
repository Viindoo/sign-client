# Viindoo Sign Client

<div align="center">

![Viindoo Sign Client](https://img.shields.io/badge/Version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**Digital Signing Application for Viindoo/Odoo Integration**

*Secure, cross-platform digital signing using USB Token/Smart Card*

</div>

---

## 📋 Overview

**Viindoo Sign Client** is a desktop application that enables digital document signing directly from your local machine. It integrates seamlessly with the [`viin_sign`](https://viindoo.com/vi/apps/app/17.0/viin_sign) module in Odoo, allowing you to sign PDF documents using:

- 🔐 **USB Token/Smart Card** (PKCS#11)
- 🖥️ **Windows Certificate Store**
- 📱 **Hardware Security Modules (HSM)**

### ✨ Key Features

- **🔒 Secure Signing**: Industry-standard PKCS#11 and X.509 certificate support
- **🌐 Cross-Platform**: Native support for Windows, Linux, and macOS
- **⚡ Real-time Integration**: WebSocket API for seamless Odoo connectivity
- **🎨 User-Friendly**: Clean, intuitive desktop interface
- **🔄 Auto-Updates**: Built-in update mechanism
- **📄 PDF Support**: Full PDF signing with visual signatures and timestamps

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10** (automatically installed by our scripts)
- **Internet connection** for initial setup
- **USB Token/Smart Card** (for hardware-based signing)

### Installation

Choose your operating system:

<details>
<summary><strong>🪟 Windows</strong></summary>

#### Automatic Installation (Recommended)

1. **Download** the latest release from [GitHub](https://github.com/Viindoo/sign-client/releases)
2. **Extract** the ZIP file to your desired location
3. **Navigate** to the `install_script` folder
4. **Run** `windows.bat`
5. **Follow** the on-screen instructions

#### Manual Installation

1. Install **Python 3.10** from [Microsoft Store](https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5)
2. Install **Microsoft Visual C++ 14** from [Microsoft](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
3. Run `python3.10 windows_installer.py` in the `install_script` folder

#### After Installation

- **Desktop Shortcut**: Click the "Viindoo Sign Client" icon
- **Start Menu**: Search for "Viindoo Sign Client"
- **Command Line**: `python3.10 main.py`

</details>

<details>
<summary><strong>🐧 Linux (Ubuntu/Debian)</strong></summary>

#### Automatic Installation (Recommended)

1. **Download** the latest release from [GitHub](https://github.com/Viindoo/sign-client/releases)
2. **Extract** the ZIP file to your desired location
3. **Navigate** to the `install_script` folder
4. **Run** `bash linux.sh`
5. **Follow** the on-screen instructions

#### Manual Installation

1. Install Python 3.10 and dependencies:
   ```bash
   sudo apt update
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install python3.10 python3.10-venv python3.10-tk
   ```
2. Run `python3.10 linux_installer.py` in the `install_script` folder

#### After Installation

- **Applications Menu**: Search for "Viindoo Sign Client"
- **Command Line**: `./bin.sh` or `python3.10 main.py`

</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

#### Automatic Installation (Recommended)

1. **Download** the latest release from [GitHub](https://github.com/Viindoo/sign-client/releases)
2. **Extract** the ZIP file to your desired location
3. **Navigate** to the `install_script` folder
4. **Run** `bash macos.sh`
5. **Follow** the on-screen instructions

#### Manual Installation

1. Install [Homebrew](https://brew.sh/) if not already installed
2. Install Python 3.10 and dependencies:
   ```bash
   brew install python@3.10 python-tk@3.10 pkg-config
   ```
3. Run `python3.10 macos_installer.py` in the `install_script` folder

#### After Installation

- **Applications Folder**: "Viindoo Sign Client.app"
- **Command Line**: `./bin.sh` or `viin-sign-client`

</details>

---

## 🗑️ Uninstallation

Choose your operating system:

<details>
<summary><strong>🪟 Windows</strong></summary>

1. **Navigate** to the `uninstall_script` folder
2. **Run** `windows.bat`
3. **Confirm** removal when prompted
4. **Choose** what to keep or remove (data, virtual environment)

</details>

<details>
<summary><strong>🐧 Linux (Ubuntu/Debian)</strong></summary>

1. **Navigate** to the `uninstall_script` folder
2. **Run** `bash linux.sh`
3. **Confirm** removal when prompted
4. **Choose** what to keep or remove (data, virtual environment, system services)

</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

1. **Navigate** to the `uninstall_script` folder
2. **Run** `bash macos.sh`
3. **Confirm** removal when prompted
4. **Choose** what to keep or remove (data, virtual environment, App Bundle)

</details>

---

## 🔧 Configuration

### USB Token/Smart Card Setup

1. **Install** your token's PKCS#11 library
2. **Connect** your USB token to your computer
3. **Launch** Viindoo Sign Client
4. **Select** "PKCS#11" as signing method
5. **Browse** to your PKCS#11 library path
6. **Enter** your PIN when prompted

### Windows Certificate Store

1. **Import** your certificate to Windows Certificate Store
2. **Launch** Viindoo Sign Client
3. **Select** "Windows Certificate" as signing method
4. **Choose** your certificate from the list

---

## 🔗 Integration with Odoo

### Viindoo Sign Module

This client integrates with the `viin_sign` Odoo module:

1. **Install** the `viin_sign` module in your Odoo instance
2. **Configure** the module settings
3. **Launch** Viindoo Sign Client on user machines
4. **Start** signing documents directly from Odoo

### API Endpoints

The client exposes a WebSocket API for Odoo integration:

- **Sign Document**: `POST /api/v1/sign`
- **Get Certificates**: `GET /api/v1/certificates`
- **Health Check**: `GET /api/v1/health`

---

## 🐛 Troubleshooting

Check the log file at `data_dir/log.txt` for detailed error logs.

---

<div align="center">

**Made with ❤️ by the Viindoo Team**

[Website](https://viindoo.com) • [Documentation](https://viindoo.com/documentation) • [Support](mailto:support@viindoo.com)

</div>