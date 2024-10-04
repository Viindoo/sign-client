if ! command -v python3.10 &>/dev/null; then
  echo "Install python3.10"
  sudo apt update
  sudo apt install software-properties-common -y
  sudo add-apt-repository ppa:deadsnakes/ppa -y
  sudo apt update
  sudo apt install python3.10 -y
fi

if ! dpkg -s python3.10-venv &>/dev/null; then
  echo "Installing python3.10 venv"
  sudo apt install python3.10-venv -y
fi
sudo apt-get install python3.10-tk
sudo python3 linux_installer.py
