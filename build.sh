#!/bin/bash

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "🧠 Downloading TextBlob corpora..."
python -m textblob.download_corpora
