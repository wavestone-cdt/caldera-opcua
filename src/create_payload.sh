#!/bin/bash
# This script creates a payload file for the specified target.
# Usage: ./create_payload.sh <name_of_script.py>

# Name of the Python script to convert
SCRIPT_NAME=opcua_scan.py

# Check if the Python script exists
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "The file $SCRIPT_NAME does not exist."
    exit 1
fi

# Run PyInstaller to create the executable
pyinstaller --onefile "$SCRIPT_NAME" --distpath dist --workpath build --name "opcua_cli" --clean $2

# Check if PyInstaller succeeded
if [ $? -eq 0 ]; then
    echo "PyInstaller successfully created the executable."

    # Remove the build directory
    rm -rf build
    echo "The build directory has been removed."
else
    echo "PyInstaller failed."
    exit 1
fi

# Move the executable to the payload directory
if [ -d "dist" ]; then
    mv -u dist/opcua_cli ../payloads/opcua_cli
    echo "The executable has been moved to the payload directory."
else
    echo "The dist directory does not exist."
    exit 1
fi
# Clean the dist directory
rm -rf dist
echo "The dist directory has been cleaned."

