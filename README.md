Project 5: Linux Server Configuration
=====================================

This is just a README file with details about Udacity's Full-Stack Web Developer Nanodegree project for configuring a base instalation of Linux on a virtual machine to host a web application.

The app hosted is the Item Catalog application available at https://github.com/pt314/udacity-fsnd-p3-item-catalog


Accessing the server
--------------------

Udacity provided a [development environment][1] on AWS.

To access the server the first time, downloaded private key and connected as `root` using ssh:
```
mv ~/Downloads/udacity_key.rsa ~/.ssh/
chmod 600 ~/.ssh/udacity_key.rsa
ssh -i ~/.ssh/udacity_key.rsa root@SERVER_IP
```
Note: For chmod to work using Cygwin on Windows, had to do `chgrp -R Users ~/.ssh`; see [chmod 600 using Cygwin and Windows][2]

Remote root access has been disabled and a `catalog` user has been created with its own SSH key. To access the server use:
```
ssh -p SSH_PORT -i ~/.ssh/udacity_key_catalog catalog@SERVER_IP
```
For this to work, the private key file `udacity_key_catalog` is required (only provided to grader).


User management
---------------

- Created `catalog` user.
  ```
  adduser catalog
  ```

- Gave sudo permissions to `catalog` user.
  ```
  cd /etc/sudoers.d/
  touch catalog
  chmod 440 catalog
  ```

  Edit `catalog` file and add line:
  ```
  student ALL=(ALL) NOPASSWD:ALL
  ```

- Password is required for `catalog` user when using sudo (using default timeout).
  ```
  nano /etc/sudoers.d/catalog
  ```

  Edit file and remove `NOPASSWD`:
  ```
  student ALL=(ALL) ALL
  ````

- Remote login of `root` user is disabled.
  ```
  nano /etc/ssh/sshd_config
  ```
  
  Set:
  ```
  PermitRootLogin no
  ```
  
  Then:
  ```
  service ssh restart
  ```
  
  Warning: Make sure you can access the server with other user before disabling this.



Security
--------

0. Generated new key pair for user `catalog`:

  - By doing this the user does not have to have the `root` user's key. For this project it does not matter since the `catalog` user is the only user and it has full sudo access, but in general this is better.

  - Keys generated on personal computer (not on server) to keep the private key private, using `ssh-keygen` and saving to file `~/.ssh/udacity_key_catalog`. This generates a file `udacity_key_catalog` with the private key and a file `udacity_key_catalog.pub` with the public key. Read `man ssh-keygen` for more details.

  - Add public key to server:
    ```
    cd /home/catalog
    mkdir .ssh
    touch .ssh/authorized_keys
    nano .ssh/authorized_keys
    ```
   
    Paste public key inside the `authorized_keys` file.
   
    ```
    chmod 700 .ssh
    chmod 644 .ssh/authorized_keys
    chown catalog:catalog -R .ssh
    service ssh restart
    ```

1. SSH is hosted on non-default port.
   
    - Edit config file:
      `sudo nano /etc/ssh/sshd_config`
   
    - Set port number:
      ```Port SSH_PORT```
   
    - Then restart SSH:
      ```service ssh restart```

2. Firewall configured to only allow connections for SSH (port SSH_PORT), HTTP (port 80), and NTP (port 123).
   
    - To start, make sure the firewall is disabled with `sudo ufw status`.
   
    - Configure general rules:
      ```
      sudo ufw default deny incoming
      sudo ufw default allow outgoing
      ```
    
    - Allow connections for SSH (port SSH_PORT), HTTP (default port 80), and NTP (default port 123):
      ```
      sudo ufw allow SSH_PORT/tcp
      sudo ufw allow www
      sudo ufw allow ntp
      sudo ufw show added
      ```
    
    - Enable the firewall and make sure it is active:
      ```
      sudo ufw enable
      sudo ufw status
      ```
    
    * Warning: Make sure you are connected over port SSH_PORT before doing this.

3. Key-based SSH authentication is enforced.
   
    - Edit config file:
      `sudo nano /etc/ssh/sshd_config`
    
    - Set port number:
      ```PasswordAuthentication no```
    
    - Then restart SSH
      ```service ssh restart```
    
    * Warning: Make sure you can access the server with the SSH key before doing this.

4. Applications have been updated to most recent updates.

   Pending...



[1]: https://www.udacity.com/account#!/development_environment "My Udacity's development environment"
[2]: http://superuser.com/questions/397288/using-cygwin-in-windows-8-chmod-600-does-not-work-as-expected "Using Cygwin in Windows 8, chmod 600 does not work as expected?"