#!/bin/sh

#https://phoenixnap.com/kb/how-to-install-python-3-ubuntu

#sudo apt-get install python3-venv

# sudo apt-get install nginx

#commented out below scripts temp
mkdir /storage
mkdir /downloads

# setup instance
#commented out below scripts temp
apt update
apt install -y nodejs
apt install -y npm
npm i -g yarn
yarn
yarn build
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3
apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
apt install python3-pip
apt-get install python3-venv
install --upgrade pip
apt-get install git
apt install -y nginx
#
apt update

# setup libs for the app
cd api

#python3 -m venv venv
#source venv/bin/activate

python3 -m venv env
#venv\Scripts\activate
source env/bin/activate

pip3 install -r requirements.txt

mkdir ./api/optimizer
git clone https://gitlab.com/yathindra/fastai1.git
git clone https://github.com/lessw2020/Best-Deep-Learning-Optimizers.git
cp ./Best-Deep-Learning-Optimizers/diffgrad/diffgrad.py ./api/optimizer/DiffGradOptimizer.py
rm -rf ./Best-Deep-Learning-Optimizers

cd ..

cp ./adapttext.service /etc/systemd/system/adapttext.service
systemctl daemon-reload

sudo rm /etc/nginx/sites-enabled/default
cp ./adapttext.nginx /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/adapttext.nginx /etc/nginx/sites-enabled/adapttext.nginx
sudo systemctl reload nginx