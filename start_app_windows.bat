@echo off

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Set environment variables
echo Configuring environment variables...
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

REM Start Flask app
echo Starting Flask server...
flask run --host=0.0.0.0 --port=5000
