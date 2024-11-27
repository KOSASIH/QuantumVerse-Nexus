#!/bin/bash

# setup_environment.sh
# Script to set up the development environment for QuantumVerse-Nexus

echo "Setting up the development environment..."

# Update package list
sudo apt-get update

# Install necessary packages
sudo apt-get install -y python3 python3-pip git

# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js and npm (if needed)
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install additional Node.js packages (if needed)
npm install

echo "Development environment setup complete!"
