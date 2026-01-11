#!/bin/bash

# -----------------------------
# IP2Location DB1 Updater
# -----------------------------

# Change this URL to your personal download link if needed
DOWNLOAD_URL="https://www.ip2location.com/download/?token=yes&file=DB9LITEBIN"

# Define filenames
ZIP_FILE="IP2LOCATION-LITE-DB9.BIN.ZIP"
BIN_FILE="IP2LOCATION-LITE-DB9.BIN"

echo "Downloading latest IP2Location DB1..."
curl -L -o "$ZIP_FILE" "$DOWNLOAD_URL"

if [ $? -ne 0 ]; then
    echo "Download failed!"
    exit 1
fi

echo "Unzipping BIN file..."
unzip -o "$ZIP_FILE"

if [ ! -f "$BIN_FILE" ]; then
    echo "Unzip failed or $BIN_FILE not found."
    exit 1
fi

echo "Cleaning up ZIP..."
rm "$ZIP_FILE"

echo "Update complete. BIN file ready: $BIN_FILE"

