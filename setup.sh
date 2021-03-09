#!/bin/sh

#https://phoenixnap.com/kb/how-to-install-python-3-ubuntu

#sudo apt-get install python3-venv

# sudo apt-get install nginx

#commented out below scripts temp
mkdir /storage
chmod 777 /storage
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
apt install -y python3-pip
apt-get install -y python3-venv
install --upgrade pip
apt-get install git
apt install -y nginx
apt install -y libmysqlclient-dev
#
apt update

# git clone https://gitlab.com/yathindra/fastai1.git

# setup libs for the app
cd api

#python3 -m venv venv
#source venv/bin/activate

python3 -m venv env
source env/bin/activate

pip install --upgrade setuptools

pip3 install blinker==1.4 wrapt==1.12.1 smart-open==3.0.0 inflection==0.3.1 wikiextractor==0.01 flask-mail==0.9.1

pip3 install -r requirements.txt

pip3 install flask-mail==0.9.1
pip3 install flask==1.1.2
pip3 install flask_cors
pip3 install flask_sqlalchemy
pip3 install flask-praetorian

mkdir resources
chmod 777 resources

flask init_database
flask add_user test test123
flask add_user yathindra yathindra123

touch /home/thilisadunik/adapttext/api/error.log
chmod 777 /home/thilisadunik/adapttext/api/error.log

mkdir optimizer
# PS : comment this out and clone this to the root in react root, only in web app
# git clone https://gitlab.com/yathindra/fastai1.git
git clone https://github.com/lessw2020/Best-Deep-Learning-Optimizers.git
cp ./Best-Deep-Learning-Optimizers/diffgrad/diffgrad.py ./optimizer/DiffGradOptimizer.py
rm -rf ./Best-Deep-Learning-Optimizers
cd pipeline
git clone https://gitlab.com/yathindra/fastai1.git
cd ..
cd ..

cp ./adapttext.service /etc/systemd/system/adapttext.service
systemctl daemon-reload
systemctl enable adapttext.service
systemctl start adapttext.service

rm /etc/nginx/sites-enabled/default
cp ./adapttext.nginx /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/adapttext.nginx /etc/nginx/sites-enabled/adapttext.nginx
systemctl reload nginx