# Update and install dependencies
echo "Setting up the environment..."
apt update && apt install -y python3 python3-venv python3-pip

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
echo "Installing dependencies..."
pip install -r requirements.txt
