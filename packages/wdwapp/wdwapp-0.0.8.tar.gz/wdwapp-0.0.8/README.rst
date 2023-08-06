Weather Data Web application
============================

For the moment, only cron.py works.
The rest of this README file is not relevant.
Please look into cron.py for explanations.
Wait next releases to have full description.

In one word :

Install this software (For fedora)
$ sudo dnf install python3-pip
$ sudo dnf install mariadb-devel
$ sudo dnf install gcc
$ sudo dnf install redhat-rpm-config
$ pip install wdwapp

Download development.ini file from : http://static.frkb.fr/wdwapp
Exemple. Do : wget http://static.frkb.fr/wdwapp/development.ini

Adapt this file for your need.

Create a database (empty) for this app.
In phpMyAdmin for exemple you can do :
CREATE USER 'wdwapp'@'localhost' IDENTIFIED BY 'my secret password';
GRANT USAGE ON *.* TO 'wdwapp'@'localhost' REQUIRE NONE WITH
MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0
MAX_USER_CONNECTIONS 0;CREATE DATABASE IF NOT EXISTS `wdwapp`;GRANT ALL
PRIVILEGES ON `wdwapp`.* TO 'wdwapp'@'localhost';

Create tables :
$ wdwapp_initialize_db development.ini

Put in a cron job this command :
$ wdwapp_cron /path/to/development.ini

Because by default data is saved every 15 minutes, it is a good idea to call
the cron job 3 minutes after. This mean every hour at 3, 18, 33 and 48 minute.
To do tis with con insert this line in the crontab :
3,18,33,48  *  *  *  * wdwapp_cron /path/to/development.ini

Start web server :
$ gunicorn --paste development.ini



DO NOT USE the rest of this file =============================================

Getting Started
---------------

- Change directory into your newly created project::

    cd meteoweb

- Create a Python virtual environment::

    python3 -m venv env

- Upgrade packaging tools::

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements::

    env/bin/pip install -e ".[testing]"

- Run your project's tests::

    env/bin/pytest

- Download ini files::

    wget http://static.frkb.fr/wdwapp/development.ini
    wget http://static.frkb.fr/wdwapp/production.ini

- Adapt ``domaines`` entry in ``[app:main]`` section from ini file
	see on https://api.ovh.com/ how to obtain keys.
	 Or go directly to https://api.ovh.com/createToken/index.cgi

- Run your project::

    env/bin/pserve development.ini
    or
    env/bin/pserve production.ini

- Acces your project:

  http://localhost:6543

- Retrieve weather data using a cron job.

   Get the URL http://localhost:6543/cron every 15 minutes.
   The best way is to add the following line in a crontab :

   */15  *  *  *  * wget -q -O /dev/null http://dev.local:6543/cron

   Replace dev.local:6543 with your domain if you have one.
   The interval used to call this service determine the data interval.

   
