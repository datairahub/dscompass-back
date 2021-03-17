# Protection Defenders Backend

Protection defenders backend are two Django apps and "datacrypter", our implementation of pycryptodome

Requires: Python 3.9

## Installation guide [Debian/Ubuntu]

On https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04 there is a well-documented ubuntu/django/uwsgi/nginx guide whose structure I usually use. It explains how to install several projects on an independent and easy-to-configure way.

##### Python

These packages will be required:
```
sudo apt-get install python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-apt libjpeg-dev \
     python3-mysqldb libmysqlclient-dev
```

##### MySQL

> More details on https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

1. Update the package index
```
sudo apt update
```

2. Install the mysql-server package:
```
sudo apt install mysql-server
```
Debian
```
sudo apt install default-mysql-server libmariadb-dev
```

3. Run the security script with sudo:
```
sudo mysql_secure_installation
```

4. Access to mysql
```
sudo mysql
```

5. Create a user:
```
CREATE USER 'CharlesDarwin'@'localhost' IDENTIFIED BY '<password>';
```

6. Create a database:
```
CREATE DATABASE `dscompass`
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;
```

7. Grant privileges:
```
GRANT ALL PRIVILEGES ON dscompass.* TO CharlesDarwin@localhost;
```

8. Flush privileges
```
FLUSH PRIVILEGES;
```

9. Exit mysql and test user login:
```
exit
mysql -u CharlesDarwin -p
```


##### Backend (Django app)

1. Go to `/srv/www/` and clone the repo:
```
git clone https://github.com/Saigesp/protectiondefenders-back.git
```

2. Install pip:
```
sudo apt install python3-pip
```

3. Check the installed pip version:
```
pip3 -V
```

4. Install **virtualenvwrapper**:
```
sudo pip3 install virtualenv virtualenvwrapper
```

5. Create a virtual environment dir:
```
sudo mkdir /srv/virtualenvs
```

6. Add the following line to `~/.bashrc` to load virtualenv commands on start:
```
export WORKON_HOME=/srv/virtualenvs
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
. /usr/local/bin/virtualenvwrapper.sh
```

7. Refresh console (or close and open it):
```
source ~/.bashrc
```

8. Create a new environment with python 3
```
mkvirtualenv --python=/usr/bin/python3 dscompass
```

9. Once created the environment is activated, so inactive it
```
deactivate
```

10. Open the environment post-activation script to edit it:
```
nano /srv/virtualenvs/dscompass/bin/postactivate
```

11. Add the following lines:
```
export CIPHER_SECRET_KEY=<your_cipher_secret_key>
export DJANGO_SECRET_KEY=<your_django_app_secret_key>

export DJANGO_DB_NAME=<your_database_name>
export DJANGO_DB_USER=<your_database_user>
export DJANGO_DB_PASSWORD=<your_database_password>

export DJANGO_EMAIL_HOST=<the_smpt_server_host>
export DJANGO_EMAIL_PORT=<the_smpt_server_port>
export DJANGO_EMAIL_HOST_USER=<the_smpt_server_user>
export DJANGO_EMAIL_HOST_PASSWORD=<the_smpt_server_password>

cd /srv/www/protectiondefenders-back/
```

9. Active the environment (you will be moved to /srv/www/protectiondefenders-back/):
```
workon dscompass
```

10. Install dependencies:
```
pip3 install -r requirements.txt
```
> If the command throw errors, try running `sudo apt-get install python3.9-dev`, `sudo apt-get install python3-setuptools` and `pip3 install --upgrade setuptools`


11. Check installation with development variables
```
python3 manage.py runserver
```
> It will show an alert about unmigrated tables, don't mind it


12. Check installations with production variables
```
python3 manage.py runserver --settings=src.protection_defenders.project_settings.settings_production
```
> If "No module named 'MySQLdb'" error appears, try running `pip install mysqlclient`

13. Migrate database:
```
python3 manage.py makemigrations defenders_auth defenders_app --settings=src.protection_defenders.project_settings.settings_production
python3 manage.py migrate --settings=src.protection_defenders.project_settings.settings_production
```

14. Collect static files
```
python manage.py collectstatic --settings=src.protection_defenders.project_settings.settings_production
```

15. Create superuser
```
python manage.py createsuperuser
```


##### uWSGI

1. Install uwsgi globally:
```
deactivate
sudo -H pip3 install uwsgi
```

2. Create configuration files:
```
sudo nano /etc/uwsgi/apps-available/dscompass.ini
```

3. Copy the following lines and save the file:
```
[uwsgi]

chdir = /srv/www/protectiondefenders-back 
home = /srv/virtualenvs/dscompass 
module = src.protection_defenders.project_wsgi:application

master = true
processes = 5

socket = /run/uwsgi/dscompass.sock
chown-socket = saigesp:www-data
chmod-socket = 660
vacuum = true

env=CIPHER_SECRET_KEY=<secret_key>
env=DJANGO_SECRET_KEY=<secret_key>

env=DJANGO_DB_NAME=<database_name>
env=DJANGO_DB_USER=<database_user>
env=DJANGO_DB_PASSWORD=<database_user_password>

env=DJANGO_EMAIL_PORT=<smtp_server_port>
env=DJANGO_EMAIL_HOST_USER=<your_email>
env=DJANGO_EMAIL_HOST_PASSWORD=<your_password>
```
> CIPHER_SECRET_KEY and DJANGO_SECRET_KEY must be equal, an use only letters and numbers

4. Create a symlink to enable it:
```
sudo ln -s /etc/uwsgi/apps-available/dscompass.ini /etc/uwsgi/apps-enabled/
```

5. Create a service file `/etc/systemd/system/uwsgi.service`:
```
[Unit]
Description=uWSGI Emperor service

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown saigesp:www-data /run/uwsgi'
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/apps-enabled
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

6. Then start the uwsgi servie
```
sudo systemctl start uwsgi
sudo systemctl enable uwsgi
```

Troubleshooting: Make sure that `/usr/local/bin/uwsgi` is executable:
```
sudo chmod +x /usr/local/bin/uwsgi
```

##### Nginx (reverse proxy)

1. Install Nginx
```
sudo apt-get install nginx
```

2. Create a new configuration file
```
sudo nano /etc/nginx/sites-available/dscompass
```

3. Copy these lines and save the file:
```
server {
    server_name ds-compass-api.protectioninternational.org;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /srv/www/protectiondefenders-back;
    }
    location /media {
       add_header Access-Control-Allow-Origin *;
       alias /srv/www/protectiondefenders-back/media/;
    }
    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/run/uwsgi/dscompass.sock;
    }
}
```

4. Link the configuration file to Nginx’s sites-enabled directory to enable them:
```
sudo ln -s /etc/nginx/sites-available/dscompass /etc/nginx/sites-enabled
```
> To disable the site, simply remove the link on sites-enabled directory


5. Check the configuration syntax by typing:
```
sudo nginx -t
```

6. Then restart the Nginx service
```
sudo systemctl restart nginx
```

7. Allow ufw acces to nginx:
```
sudo ufw allow 'Nginx Full'
```

## Let's encrypt (optional)

1. Install Certbot
```
sudo apt install certbot python3-certbot-nginx
```

2. Obtain the certificate
```
sudo certbot --nginx -d ds-compass.protectioninternational.org
```

Renew certificates
```
sudo certbot renew
```