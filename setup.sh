#!/bin/bash

# Make sure the data directory exists
mkdir -p data

# Create necessary configuration directory
mkdir -p .streamlit

# Create the config file if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
    echo "[server]" > .streamlit/config.toml
    echo "headless = true" >> .streamlit/config.toml
    echo "address = \"0.0.0.0\"" >> .streamlit/config.toml
    echo "port = 5000" >> .streamlit/config.toml
fi

echo "Setup complete!"