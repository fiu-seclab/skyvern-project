#!/bin/bash

# Script to copy SKYVERN_API_KEY from .env to skyvern/skyvern-frontend.env as VITE_SKYVERN_API_KEY

set -e  # Exit on any error

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found in current directory"
    exit 1
fi

# Extract SKYVERN_API_KEY value from .env
API_KEY=$(grep "^SKYVERN_API_KEY=" .env | cut -d '=' -f2- | tr -d '"' | tr -d "'")

# Check if API key was found
if [ -z "$API_KEY" ]; then
    echo "Error: SKYVERN_API_KEY not found in .env file"
    exit 1
fi


# Path to the frontend env file
FRONTEND_ENV_FILE="skyvern/skyvern-frontend/.env"

# Check if frontend env file exists
if [ -f "$FRONTEND_ENV_FILE" ]; then
    # Update existing file - remove old VITE_SKYVERN_API_KEY if it exists and add new one
    grep -v "^VITE_SKYVERN_API_KEY=" "$FRONTEND_ENV_FILE" > "${FRONTEND_ENV_FILE}.tmp" || true
    echo "VITE_SKYVERN_API_KEY=$API_KEY" >> "${FRONTEND_ENV_FILE}.tmp"
    mv "${FRONTEND_ENV_FILE}.tmp" "$FRONTEND_ENV_FILE"
    echo "Successfully updated VITE_SKYVERN_API_KEY in existing $FRONTEND_ENV_FILE"
else
    # Create new file with just the API key
    echo "VITE_SKYVERN_API_KEY=$API_KEY" > "$FRONTEND_ENV_FILE"
    echo "Successfully created $FRONTEND_ENV_FILE with VITE_SKYVERN_API_KEY"
fi