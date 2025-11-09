#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Installing system packages for audio playback and LED matrix..."
sudo apt-get update
sudo apt-get install -y python3-dev python3-venv python3-pip libopenjp2-7 libtiff6 mpg123

echo "If not already installed, clone and build rpi-rgb-led-matrix from:\n  https://github.com/hzeller/rpi-rgb-led-matrix"

python3 -m venv "$PROJECT_ROOT/.venv"
source "$PROJECT_ROOT/.venv/bin/activate"

pip install --upgrade pip
pip install -r "$PROJECT_ROOT/requirements.txt"

echo "Dependencies installed. Activate the virtual environment with:"
echo "  source $PROJECT_ROOT/.venv/bin/activate"


