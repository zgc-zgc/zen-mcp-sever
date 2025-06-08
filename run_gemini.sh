#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python gemini_server.py "$@"