#!/bin/bash
# Update system
sudo dnf update -y

# Install Git
sudo dnf install git -y

# Clone your repo
cd /home/ec2-user
git clone https://github.com/harishkemkar/XL_Analysis
cd XL_Analysis

# Install Python 3.11
sudo dnf install python3.11 -y

# Check version
python3.11 --version

# Create virtual environment
python3.11 -m venv venv

# Activate venv
source venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

# Run the app with Gunicorn (background mode)
cd /home/ec2-user/XL_Analysis
source venv/bin/activate
nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app > gunicorn.log 2>&1 &