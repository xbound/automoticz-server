#!/bin/bash
# Clean Python .pyc files
sudo find . -type f -name "*.py[co]" -delete
sudo find . -type d -name "__pycache__" -delete