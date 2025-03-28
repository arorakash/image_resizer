# Activate virtual environment
echo "Activating virtual environment..."
# python3 -m venv venv
source venv/bin/activate

# Export environment variables
echo "Configuring environment variables..."
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Start Flask app
echo "Starting Flask server..."
flask run --host=0.0.0.0 --port=5000
