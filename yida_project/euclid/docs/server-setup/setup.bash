# Update the whole environment
sudo apt-get -y update
sudo apt-get -y upgrade

# Install software
sudo apt-get -y install python3-setuptools python3-dev build-essential unzip python3-pip virtualenv gunicorn nginx rabbitmq-server
sudo pip3 install --upgrade pip3

# after install gunicorn
pip install -r requirement.txt