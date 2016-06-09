Project 5: Linux Server Configuration
=====================================

This is just a README file with details about Udacity's Full-Stack Web Developer Nanodegree project for configuring a base instalation of Linux on a virtual machine to host a web application.

The app hosted is the Item Catalog application available at https://github.com/pt314/udacity-fsnd-p3-item-catalog

Note that this is a log of changes made. Some things may not apply later if the application is modified later, and the application will only be available temporarily on the web server. Also, this is a learning project, so suggestions welcome :)

For some time the application is available at http://ec2-52-36-197-127.us-west-2.compute.amazonaws.com/


App and server info
-------------------

Replace these constants when reading the text below.

- APP_URL = http://ec2-52-36-197-127.us-west-2.compute.amazonaws.com/
- SERVER_NAME = ec2-52-36-197-127.us-west-2.compute.amazonaws.com
- SERVER_IP = 52.36.197.127
- SSH_PORT = 2200


Accessing the server
--------------------

Udacity provided a [development environment][1] on AWS.

To access the server the first time, downloaded private key and connected as `root` using ssh:
```
mv ~/Downloads/udacity_key.rsa ~/.ssh/
chmod 600 ~/.ssh/udacity_key.rsa
ssh -i ~/.ssh/udacity_key.rsa root@SERVER_IP
```
Note: For chmod to work using Cygwin on Windows, had to do `chgrp -R Users ~/.ssh` (see [chmod 600 using Cygwin and Windows][2]).

Remote root access has been disabled and a `catalog` user has been created with its own SSH key. To access the server use:
```
ssh -p SSH_PORT -i ~/.ssh/udacity_key_catalog catalog@SERVER_IP
```
For this to work, the private key file `udacity_key_catalog` is required (only provided to grader).


Summary of changes
------------------

This is a short summary of changes. More details can be found below.

- Created `catalog` user for running the application with its own SSH key.
- The `catalog` user has sudo permissions and password is required with using sudo.
- Remote login of `root` user is disabled.
- SSH is hosted on a non-default port and SSH authentication is enforced.
- Firewall configured to only allow connections for SSH (port SSH_PORT), HTTP (port 80), and NTP (port 123).
- Applications have been updated.
- [PostgreSQL][4] has been installed and configured as the database server.
- [Apache][8] web server and [mod_wsgi][9] have been installed.
- Other packages required by the application have been installed.
- Item Catalog application has been setup.

Some possible improvements:

- Using UFW rate limiting to prevent brute force attacks.
- Configuring backup (definitely at least for the database).
- Apache status monitoring with mod_status module.
- System monitoring with [Munin][12] or [Nagios][13]. 


User management
---------------

1. Created `catalog` user with sudo permissions:

    - Create user:
      ```
      $ adduser catalog
      ```

    - Create sudo config file:
      ```
      $ cd /etc/sudoers.d/
      $ touch catalog
      $ chmod 440 catalog
      ```

    - Edit `catalog` file and add line:
      ```
      student ALL=(ALL) NOPASSWD:ALL
      ```

2. Password is required for `catalog` user when using sudo (using default timeout).
  
    - Edit sudoers file:
      ```$ nano /etc/sudoers.d/catalog```

    - Make sure `NOPASSWD` is removed:
      ```student ALL=(ALL) ALL```

3. Remote login of `root` user is disabled.

    - Edit config file:
      ```$ nano /etc/ssh/sshd_config```
   
    - Set login option:
      ```PermitRootLogin no```
   
    - Then restart SSH:
      ```$ service ssh restart```
  
  Warning: Make sure you can access the server with another user before disabling this.


Security
--------

1. Generated new key pair for user `catalog`:

    - By doing this the user does not have to have the `root` user's key. For this project it does not matter since the `catalog` user is the only user and it has full sudo access, but in general this is better.

    - Keys generated on personal computer (not on server) to keep the private key private, using `ssh-keygen` and saving to file `~/.ssh/udacity_key_catalog`. This generates a file `udacity_key_catalog` with the private key and a file `udacity_key_catalog.pub` with the public key. Read `man ssh-keygen` for more details.

    - Add public key to server:
      ```
      $ cd /home/catalog
      $ mkdir .ssh
      $ touch .ssh/authorized_keys
      $ nano .ssh/authorized_keys
      ```
   
    - Paste public key inside the `authorized_keys` file.
      ```
      $ chmod 700 .ssh
      $ chmod 644 .ssh/authorized_keys
      $ chown catalog:catalog -R .ssh
      $ service ssh restart
      ```

2. SSH is hosted on non-default port.
   
    - Edit config file:
      ```$ sudo nano /etc/ssh/sshd_config```
   
    - Set port number:
      ```Port SSH_PORT```
   
    - Then restart SSH:
      ```$ service ssh restart```

3. Firewall configured to only allow connections for SSH (port SSH_PORT), HTTP (port 80), and NTP (port 123).
   
    - To start, make sure the firewall is disabled with `sudo ufw status`.
   
    - Configure general rules:
      ```
      $ sudo ufw default deny incoming
      $ sudo ufw default allow outgoing
      ```
    
    - Allow connections for SSH (port SSH_PORT), HTTP (default port 80), and NTP (default port 123):
      ```
      $ sudo ufw allow SSH_PORT/tcp
      $ sudo ufw allow www
      $ sudo ufw allow ntp
      $ sudo ufw show added
      ```
    
    - Enable the firewall and make sure it is active:
      ```
      $ sudo ufw enable
      $ sudo ufw status
      ```
    
4. Key-based SSH authentication is enforced.
   
    - Edit config file:
      ```$ sudo nano /etc/ssh/sshd_config```
    
    - Set option:
      ```PasswordAuthentication no```
    
    - Then restart SSH
      ```$ service ssh restart```
    
    Warning: Make sure you can access the server with the SSH key before doing this.

5. Applications have been updated to most recent updates.

    - Update packages:
      ```
      $ sudo apt-get update
      $ sudo apt-get upgrade
      ```

    - Configure automatic _security_ updates (see [Ubuntu Documentation: Automatic Security Updates][3]):
      ```
      $ sudo apt install unattended-upgrades
      $ sudo dpkg-reconfigure --priority=low unattended-upgrades
      ```

    - Configure `Unattended-Upgrade::Mail` in `/etc/apt/apt.conf.d/50unattended-upgrades` to receive problem notifications.


Application
-----------

1. Database server has been configured to serve data.

    - Install [PostgreSQL][4] and [Psycopg][5] adapter for Python:
      ```
      $ sudo apt-get -qqy install postgresql python-psycopg2
      ```

    - Create database user and empty database:
      ```
      $ sudo -u postgres createuser -dRS catalog
      $ sudo -u catalog createdb catalog
      ```
      Note: Since this is a simple app with its own simple database, the Linux user is used to authenticate with the database. For more complex applications, a separate database user with its own password may be desirable.

    - Update permissions (see [StackExchange][6] and [DigitalOcean][7]):
      ```
      $ psql
      catalog=> REVOKE CONNECT ON DATABASE catalog FROM PUBLIC;
      catalog=> GRANT CONNECT ON DATABASE catalog TO catalog;
      catalog=> REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
      catalog=> GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO catalog;
      catalog=> ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO catalog;
      catalog=> ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, USAGE ON SEQUENCES TO catalog;
      ```

      Note: Privileges are given to the catalog user directly. For more complex situations, using roles may be desirable.

    - Remote connections are disabled (by default) in `/etc/postgresql/9.3/main/pg_hba.conf`

2. Web-server has been configured to serve the Item Catalog application as a wsgi app.

    - Install [Apache][8] web server and [mod_wsgi][9]:
      ```
      $ sudo apt-get update
      $ sudo apt-get install apache2
      $ sudo apt-get install libapache2-mod-wsgi
      ```

    - Install packages required by the application:
      ```
      $ sudo apt-get -qqy update
      $ sudo apt-get -qqy install python-flask python-sqlalchemy
      $ sudo apt-get -qqy install python-pip
      $ sudo pip install oauth2client
      $ sudo pip install requests
      $ sudo pip install httplib2
      $ sudo pip install redis
      $ sudo pip install passlib
      $ sudo pip install itsdangerous
      $ sudo pip install flask-httpauth
      $ sudo pip install Flask-WTF
      $ sudo pip install Flask-SQLAlchemy
      ```

    - Copy application to server (ignore vagrant and git files):
      ```
      $ sudo apt-get -qqy install git
      $ git clone https://github.com/pt314/udacity-fsnd-p3-item-catalog.git
      $ sudo cp -r udacity-fsnd-p3-item-catalog/vagrant/catalog/ /var/www/
      ```
      Alternatively clone on local computer and copy to server using `scp`:
      ```
      $ scp -rp -i ~/.ssh/udacity_key_catalog -P SSH_PORT udacity-fsnd-p3-item-catalog/vagrant/catalog/ catalog@SERVER_IP:~
      ```

    - Configure application (see configuration details in project's README):

      - Google sign-in (configure [Google Developers Console project][10] and add `client_secret_google.json`)
      - Secret keys (be sure to update these and use randomly generated secure keys, using for example [`keygen.py`](keygen.py))

      Note: Created [issue](https://github.com/pt314/udacity-fsnd-p3-item-catalog/issues/2) - Move settings to config file.

    - Allow application to write images to uploads folder:
      ```
      $ sudo chown catalog /var/www/catalog/uploads/
      ```
      Note: Created [issue](https://github.com/pt314/udacity-fsnd-p3-item-catalog/issues/1) - Ideally, files would be saved to a location outside of the application directory.

    - Initialize database (create tables and add sample data):
      ```
      $ cd /var/www/catalog/
      $ sudo -u catalog python database_setup.py
      $ sudo -u catalog python populate_database.py
      ```

    - Add [`catalog.wsgi`](catalog.wsgi) file to `/var/www/catalog/` folder:
      ```
      import sys

      app_path = "/var/www/catalog"
          if not app_path in sys.path:
          sys.path.insert(0, app_path)

      from catalog import app as application
      ```

    - Disable directory browsing:

      Edit `/etc/apache2/apache2.conf` and remove `Indexes` from `/var/www/` directory options, and restart Apache.

    - Configure Apache virtual host and enable site:

      Add [`catalog.conf`](catalog.conf) file to `/etc/apache2/sites-available` folder (see [Flask documentation][11]):
      ```
      <VirtualHost *:80>
          ServerName SERVER_NAME

          WSGIDaemonProcess catalog user=catalog group=catalog threads=5
          WSGIScriptAlias / /var/www/catalog/catalog.wsgi

          <Directory /var/www/catalog>
              WSGIProcessGroup catalog
              WSGIApplicationGroup %{GLOBAL}
              Order deny,allow
              Allow from all
          </Directory>

          ErrorLog ${APACHE_LOG_DIR}/error.log
          CustomLog ${APACHE_LOG_DIR}/access.log combined
      </VirtualHost>
      ```

      Enable site and restart Apache:
      ```
      $ sudo a2dissite 000-default
      $ sudo a2ensite catalog
      $ sudo service apache2 reload
      $ sudo apache2ctl restart
      ```

      The application should be available at the APP_URL.


[1]: https://www.udacity.com/account#!/development_environment "My Udacity's development environment"
[2]: http://superuser.com/questions/397288/using-cygwin-in-windows-8-chmod-600-does-not-work-as-expected "Using Cygwin in Windows 8, chmod 600 does not work as expected?"
[3]: https://help.ubuntu.com/community/AutomaticSecurityUpdates "Ubuntu Documentation: Automatic Security Updates"
[4]: http://www.postgresql.org/ "PostgreSQL"
[5]: http://initd.org/psycopg/ "Psycopg"
[6]: http://dba.stackexchange.com/questions/33943/granting-access-to-all-tables-for-a-user "Granting access to all tables for a user"
[7]: https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps "How To Secure PostgreSQL on an Ubuntu VPS"
[8]: https://httpd.apache.org/ "Apache webserver"
[9]: http://www.modwsgi.org/ "mod_wsgi"
[10]: https://developers.google.com/identity/sign-in/web/devconsole-project "Creating a Google Developers Console project and client ID"
[11]: http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/ "Flask documentation: mod_wsgi (Apache)"
[12]: https://www.digitalocean.com/community/tutorials/how-to-install-munin-on-an-ubuntu-vps "How To Install Munin on an Ubuntu VPS"
[13]: https://www.digitalocean.com/community/tutorials/how-to-install-nagios-4-and-monitor-your-servers-on-ubuntu-14-04 "How To Install Nagios 4 and Monitor Your Servers on Ubuntu 14.04"
