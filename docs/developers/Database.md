# Database management

##Overview
Remotelabz uses a MYSQL database that can be accessed locally on remotelabz front server at localhost:3306

By default, the MySQL database is configured with the root password : "RemoteLabz-2022$", a user "user" is also created with password "Mysql-Pa33wrd$". 

##Accessing Remotely to Database

First you need to edit the mysql configuration file `/etc/mysql/mysql.conf.d/mysqld.cnf` on the front server

set these value to :

```
bind-address        =*
mysqlx-bind-address =*
```

Then connect to the mysql server  as root.

`sudo mysql`

Then you will have to create a user that has remote access privilege and all privileges on the database
```
CREATE USER 'rlabdevel'@'%'identified by 'yourpassword'
GRANT ALL PRIVILEGES ON remotelabz.* TO 'rlabdevel'@'%' with grant option;
```
!!! Warning 
    This will expose your mysql server over your network.For security reasons,tt is recommended to choose a strong password for the user `rlabdevel`.

##Database Structure

![Screenshot](/images/Developers/remotelabz-schema-db.png)

