#!/bin/bash

source ~/.bashrc

# update conda
conda update -n base -c defaults conda -y

# Create a new conda environment
conda create -n ml python=3.9 -y

# Activate the new environment
conda activate ml

# Install specific packages in the conda environment
pip install transformers datasets fsspec s3fs python-gitlab rootpath ipykernel

# Update and upgrade apt packages
apt update
apt upgrade -y

# Install specific packages from apt
apt install vim tree git-lfs curl  -y

# install gcm 
dpkg -i downloads/gcm-linux_amd64.2.3.2.deb

# setup gcm 
git-credential-manager configure

# add default git credential storage to bash
echo export GCM_CREDENTIAL_STORE=plaintext >> ~/.bashrc
source ~/.bashrc

