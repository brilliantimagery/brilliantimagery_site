# update the system
apt update && apt upgrade -y

# set hostname
hostnamectl set-hostname <host named (jango-server)>
# test that it changed
hostname

# set hostname in host file
sudo nano /etc/hosts
# under 127.0.0.1 localhost add <system ip address> <host name (django-server)>

# add a non-root user
adduser <username>
adduser <username> sudo

# log out and back in as the new user
exit

# reboot if needed
sudo reboot

# ------------- set up SSH ------------------
# go to home directory
cd ~
# test if desisired with
pwd

# make ssh directory
mkdir .ssh

# on local machine make ssk hey
# generate ssh key
ssh-keygen -b 4096
# push ssh key to server
scp ~/.ssh/id_rsa.pub <username>@<ip address>:~/.ssh/authorized_keys

# set ssh permissions
sudo chmod 700 ~/.ssh/
sudo chmod 600 ~/.ssh/*

# log back in with ssh
exit
ssh <username>@<host ip>

# disallow root logins over ssh
sudo nano /etc/ssh/sshd_config
# change    PermitRootLogin yes > PermitRootLogin no
# change    #PasswordAuthentication yes > PasswordAuthontication no
# restart ssh service
sudo systemctl restart sshd


# change the shell
sudo apt install zsh
sudo sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Stop the hackers
sudo apt install fail2ban -y
sudo apt install ufw
# GET THIS PART RIGHT OR BE LOCKED OUT!!!!
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 8000
sudo ufw enable
# to check ufw status
sudo ufw status

# install OS dependencies
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt-get install -y -q build-essential git unzip zip nload tree
sudo apt-get install -y -q python3-pip python3.8-dev python3.8-venv
sudo apt-get install -y -q nginx
# for gzip support in uwsgi
sudo apt-get install --no-install-recommends -y -q libpcre3-dev libz-dev

# Basic git setup
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=720000'
# Be sure to put your info here:
git config --global user.email "you@email.com"
git config --global user.name "Your name"

# Web app file structure
mkdir /apps
chmod 777 /apps
mkdir /apps/logs
mkdir /apps/logs/pypi
mkdir /apps/logs/pypi/app_log
cd /apps

# Create a virtual env for the app.
cd /apps
sudo python3.8 -m pip install --upgrade pip setuptools
python3.8 -m venv venv
. /apps/venv/bin/activate
pip install --upgrade pip setuptools
pip install --upgrade httpie glances
pip install --upgrade uwsgi

# install the app
git clone https://github.com/brilliantimagery/brilliantimagery_site.git
cd brilliantimagery_site
pip install -r requirements.txt

# make a few folders
sudo mkdir /apps/brilliantimagery_site/docs
sudo mkdir /apps/brilliantimagery_site/media/profile_pics
# transfer docs from local machine
scp -r <path\to\>\brilliantimagery_site\docs\* <username>@<ip address>:/apps/docs
scp -r <path\to\>\brilliantimagery_site\bi_site\config.py <username>@<ip address>:/apps/
# move db if desired
scp -r <path\to\>\brilliantimagery_site\db.sqlite3 <username>@<ip address>:/apps/
sudo mv /apps/db.sqlite3 /apps/brilliantimagery_site/
# move transfered files
sudo mv /apps/docs/* /apps/brilliantimagery_site/docs
sudo mv /apps/config.py /apps/brilliantimagery_site/bi_site

# move the static files
cd /apps/brilliantimagery_site
python manage.py collectstatic

# test server
python manage.py runserver 0.0.0.0:8000
# test file creation, user creation, reset password, upload avatar

# Copy and enable the daemon
sudo cp /apps/brilliantimagery_site/server/bi_site.service /etc/systemd/system/bi_site.service

sudo systemctl start bi_site
sudo systemctl status bi_site
sudo systemctl enable bi_site

# CAREFUL HERE. If you are using default, maybe skip this
sudo rm /etc/nginx/sites-enabled/default

sudo cp /apps/brilliantimagery_site/server/bi_site.nginx /etc/nginx/sites-enabled/bi_site.nginx
sudo update-rc.d nginx enable
sudo service nginx restart



# reenable 'normal' port traffic
# want 80 and 443 open
sudo ufw delete allow 8000
sudo ufw allow http/tcp
sudo ufw allow 443
sudo ufw enable
sudo ufw status
sudo /etc/init.d/nginx restart

# restart uwsgi
sudo systemctl restart bi_site
# restart nginx
sudo systemctl restart nginx
