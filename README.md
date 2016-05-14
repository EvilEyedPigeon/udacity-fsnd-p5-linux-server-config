Project 5: Linux Server Configuration
=====================================

This is just a README file with details about Udacity's Full-Stack Web Developer Nanodegree project for configuring a base instalation of Linux on a virtual machine to host a web application.

The app hosted is the Item Catalog application available at https://github.com/pt314/udacity-fsnd-p3-item-catalog


Accessing the server
--------------------

Udacity provided a development environment on AWS.

To access the server, download private key, then:

```
mv ~/Downloads/udacity_key.rsa ~/.ssh/
chmod 600 ~/.ssh/udacity_key.rsa
ssh -i ~/.ssh/udacity_key.rsa root@SERVER_IP
```


User management
---------------

- Created `catalog` user.
  ```sudo adduser catalog```

- Gave sudo permissions to `catalog` user.
  ```
  cd /etc/sudoers.d/
  sudo touch catalog
  sudo chmod 440 catalog
  ```
  Edit `catalog` file and add line:
  ```
  student ALL=(ALL) NOPASSWD:ALL
  ```

- Password is required for `catalog` user when using sudo.

- Remote login of `root` user is disabled.

