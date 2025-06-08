@echo off
REM Windows batch script to run Gemini MCP server

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Activate the virtual environment and run the server
call "%SCRIPT_DIR%venv\Scripts\activate.bat"
python "%SCRIPT_DIR%gemini_server.py"