#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install Pillow
pip install colorama
clear
python AsciiFicate.py
