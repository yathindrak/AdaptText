#!/bin/sh

#https://phoenixnap.com/kb/how-to-install-python-3-ubuntu

#sudo apt-get install python3-venv

# sudo apt-get install nginx

#commented out below scripts temp
mkdir /storage
chmod 777 /storage
mkdir /downloads
mkdir /classification
chmod 777 /classification

# setup instance
#commented out below scripts temp
apt update

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
source ~/.nvm/nvm.sh
nvm install 10


# apt install -y nodejs
# apt install -y npm
npm i -g yarn
yarn
yarn build
# cp build /var/
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3
apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
sudo apt-get install gcc libpq-dev -y
apt install -y python3-pip
apt-get install -y python3-venv
install --upgrade pip
apt-get install git

wget https://nginx.org/keys/nginx_signing.key
apt-key add nginx_signing.key

echo "deb https://nginx.org/packages/mainline/ubuntu/ bionic nginx" | sudo tee -a /etc/apt/sources.list
echo "deb https://nginx.org/packages/mainline/ubuntu/ bionic nginx" | sudo tee -a /etc/apt/sources.list

apt-get update

apt-get install nginx=1.15.0-1~bionic -y

apt install -y libmysqlclient-dev
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=5557f6a687102089b482b46479d702d9 DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
#
apt update

pip3 install wheel
python3 setup.py bdist_wheel
pip3 install --upgrade setuptools
pip3 install --upgrade cython
pip3 install ddtrace==0.47.0
# git clone https://gitlab.com/yathindra/fastai1.git

# setup libs for the app
cd api

#python3 -m venv venv
#source venv/bin/activate

python3 -m venv env
source env/bin/activate

pip install wheel
python setup.py bdist_wheel

pip install --upgrade setuptools

pip3 install --upgrade cython

pip3 install blinker==1.4 wrapt==1.12.1 smart-open==3.0.0 inflection==0.3.1 wikiextractor==0.01 flask-mail==0.9.1
pip3 install numpy python-dotenv

python3 -m pip install --upgrade pip
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
cd pipeline
git clone https://github.com/lessw2020/Best-Deep-Learning-Optimizers.git
cp ./Best-Deep-Learning-Optimizers/diffgrad/diffgrad.py ./optimizer/DiffGradOptimizer.py
rm -rf ./Best-Deep-Learning-Optimizers
git clone https://gitlab.com/yathindra/fastai1.git
cd ..
cd ..

mkdir /etc/datadog-agent/conf.d/python.d
cp ./conf.yaml /etc/datadog-agent/conf.d/python.d/conf.yaml
chown -R dd-agent:dd-agent /etc/datadog-agent/conf.d/python.d/
systemctl restart datadog-agent

cp ./adapttext.service /etc/systemd/system/adapttext.service
systemctl daemon-reload
systemctl enable adapttext.service
systemctl start adapttext.service

rm /etc/nginx/sites-enabled/default
cp ./adapttext.nginx /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/adapttext.nginx /etc/nginx/sites-enabled/adapttext.nginx
systemctl reload nginx