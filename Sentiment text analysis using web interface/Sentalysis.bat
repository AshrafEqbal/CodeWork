@echo off
REM Change to the E: drive
E:

REM Start the Python server in a new command window
start "" python test.py

REM Wait for a moment to ensure the server starts (adjust delay as needed)
timeout /t 15 /nobreak >nul

REM Open the local URL in the default web browser
start "" "http://127.0.0.1:5000/"

REM Optional: Pause to keep the command window open
pause
