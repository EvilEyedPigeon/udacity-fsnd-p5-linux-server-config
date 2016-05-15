Project 5: Linux Server Configuration
=====================================

This is just a README file with details about Udacity's Full-Stack Web Developer Nanodegree project for configuring a base instalation of Linux on a virtual machine to host a web application.

The app hosted is the Item Catalog application available at https://github.com/pt314/udacity-fsnd-p3-item-catalog


Accessing the server
--------------------

Udacity provided a [development environment][1] on AWS.

To access the server the first time, downloaded private key connected as `root` using ssh:
```
mv ~/Downloads/udacity_key.rsa ~/.ssh/
chmod 600 ~/.ssh/udacity_key.rsa
ssh -i ~/.ssh/udacity_key.rsa root@SERVER_IP
```


Remote root access has been disabled and a `catalog` user has been creatd. To access the server use:
```
ssh -p SSH_PORT -i ~/.ssh/udacity_key_catalog catalog@SERVER_IP
```

For this to work, the private key file `udacity_key_catalog` is necessary (only provided to grader).


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
  Edit file:
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




[1]: https://www.udacity.com/account#!/development_environment "My Udacity's development environment"
