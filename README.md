Viindoo Sign Client
===================

This is an application that runs on the user's local machine to integrate with the `viin_sign` module, allowing digital
signing using USB Token/Smart Card, ...

How to install?
---------------

**Windows**

- Open **Microsoft Store**, search `python3.10` and install it, ignore if you have installed.
- Download and install the latest **Microsoft Visual C++ 14** from [*here*](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version), ignore if you have installed.
- Download `Viindoo Sign Client` and unzip it (or clone this repo), go to `install_script` and run `windows.bat` file.
- After installation, you can run the application from Desktop or Start Menu by clicking on **Viindoo Sign Client** shortcut.

**Linux Debian (Ubuntu, ..)**

- Download `Viindoo Sign Client` and unzip it (or clone this repo), go to `install_script` and run `linux.sh` file (To run a `.sh` file, you can type `bash sh_file.sh` to terminal).
- After that, run `bin.sh`. For ubuntu, you can run the **Viindoo Sign Client** application from Applications.

**macOS and others**
- Install `python3.10` and `python-tkinter`.
- Create a python venv 3.10 named `.venv` with same application folder.
- install `requirements.txt` for that venv and run `bin.sh` or run `main.py` with that venv.

Development
-----------

- Make a python venv (3.10), install libs in `requirements.txt` and run `main.py` file like other python projects.
