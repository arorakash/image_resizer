@echo off

REM Update and install dependencies
echo Setting up the environment...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install required Python packages
echo Installing dependencies...
pip install -r requirements.txt
