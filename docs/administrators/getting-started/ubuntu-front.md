# RemoteLabz's front installation guide

This section guides you through the installation of RemoteLabz and its components on an Ubuntu system. We assume you have already installed an Ubuntu Server 20.04 LTS.

!!! note "Foreword"

    - This section has only been tested with **Ubuntu 20.04**.
    - The first steps explains how to install [requirements](#requirements). You may skip these steps if those software are already present on your system and go to [Install RemoteLabz](#install-remotelabz).

!!! warning
    - From the version 2.2.0 of RemoteLabz, we recommand to use at least Ubuntu 20.04 (LTS)

## Retrieve the RemoteLabz source
A remotelabz directory will be create on your home directory.
```bash
cd ~
git clone https://github.com/remotelabz/remotelabz.git
```

You have now a directory `remotelabz` created on your home directory.

!!! warning
    If you want install only a specific version, you have to do the following instruction, for version 2.4.1 for example.
    ```bash    
    git clone https://github.com/remotelabz/remotelabz.git --branch 2.4.1 --single-branch
    ```
    ou
    ```bash    
    git clone https://github.com/remotelabz/remotelabz.git --branch dev
    ```

## Requirements

#### On Ubuntu 20.04 LTS
``` bash
sudo apt-get update
sudo apt install -y curl gnupg php zip unzip php-bcmath php-curl php-gd php-intl php-mbstring php-mysql php-xml php-zip ntp openvpn libapache2-mod-php7.4
```

### Configure PHP
You have to configure the php.ini of your apache2 (/etc/php/7.4/apache2/php.ini) with the following parameters :
``` bash
upload_max_filesize = 3G
post_max_size = 3G
```

and perhaps, change the `max_execution_time` if the upload is too long
``` bash
max_execution_time
```

### Composer

You may download Composer by following [official documentation](https://getcomposer.org/download/), but RemoteLabz is delivered with a copy of Composer 2.2.6 that you can copy in a `bin` folder.
``` bash
php -r "copy('https://getcomposer.org/download/2.2.6/composer.phar', 'composer.phar');"
sudo cp composer.phar /usr/local/bin/composer
sudo chmod a+x /usr/local/bin/composer
```

### Node.js
The NodeJS's version in Ubuntu 18 and above is too old. We recommand to use version 12 of NodeJS
``` bash
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Yarn
``` bash
sudo npm install -g yarn
```
### MySQL Server

#### On Ubuntu 20.04 LTS
``` bash
sudo apt-get install -y mysql-server
sudo mysql_secure_installation
```
We recommand to answer as follow :
```bash
Securing the MySQL server deployment.

Connecting to MySQL using a blank password.

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No: Y

There are three levels of password validation policy:

LOW    Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary                  file

Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 2
Please set the password for root here.

New password: RemoteLabz-2022$

Re-enter new password: RemoteLabz-2022$

Estimated strength of the password: 100 
Do you wish to continue with the password provided?(Press y|Y for Yes, any other key for No) : Y
By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) : Y
Success.


Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) : Y
Success.

By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.


Remove test database and access to it? (Press y|Y for Yes, any other key for No) : Y
 - Dropping test database...
Success.

 - Removing privileges on test database...
Success.

Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) : Y
Success.

All done!

```



``` bash
sudo mysql -u root -p
CREATE USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Mysql-Pa33wrd$';
CREATE DATABASE remotelabz;
GRANT ALL ON remotelabz.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```
Choose a secure password to your MySQL server and you have to disable the remote access to your mysql server.

!!! info
    If you need to activate the remote access to your MySQL, you have to create a user like this :
    ``` bash
    CREATE USER 'user'@'%' IDENTIFIED WITH mysql_native_password BY 'Mysql-Pa33wrd$';
    GRANT ALL ON remotelabz.* TO 'user'@'%';
    FLUSH PRIVILEGES;
    ```
### RabbitMQ

To use RabbitMQ as messaging backend, you need the **php-amqp** extension :

#### On Ubuntu 20.04 LTS
```bash
sudo apt-get install -y rabbitmq-server php-amqp
```

#### Configuration of RabbitMQ
The [worker] needs to connect to the RabbitMQ. We have to create a specific user to the RemoteLabz. Change the password 'password-amqp' in the following command
```bash
sudo rabbitmqctl add_user 'remotelabz-amqp' 'password-amqp'
sudo rabbitmqctl set_permissions -p '/' 'remotelabz-amqp' '.*' '.*' '.*'
```
Restart the RabbitMQ server
```bash
sudo service rabbitmq-server restart
```

!!! Tips
    If you want to change the password of an existing user `username` of your RabbitMQ, you have to type the following command :
    ```
    sudo rabbitmqctl change_password 'username' 'new_password'
    ```

### Configure OpenVPN

####Installation of Easy RSA 3.0
```bash
cd ~
# link to the latest version
wget https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.8/EasyRSA-3.0.8.tgz
tar -xzf EasyRSA-3.0.8.tgz
ln -s EasyRSA-3.0.8 EasyRSA
cd EasyRSA
```

####Prepare configuration files
Create the `vars` file and add the following lines. You can change the value for your organisation
```bash
#File ~/EasyRSA/vars
set_var EASYRSA_BATCH           "yes"
set_var EASYRSA_REQ_CN         "RemoteLabz-VPNServer-CA"
set_var EASYRSA_REQ_COUNTRY    "FR"
set_var EASYRSA_REQ_PROVINCE   "Grand-Est"
set_var EASYRSA_REQ_CITY       "Reims"
set_var EASYRSA_REQ_ORG        "RemoteLabz"
set_var EASYRSA_REQ_EMAIL      "contact@remotelabz.com"
set_var EASYRSA_REQ_OU         "RemoteLabz-VPNServer"
set_var EASYRSA_ALGO           "ec"
set_var EASYRSA_DIGEST         "sha512"
set_var EASYRSA_CURVE          secp384r1
#5 ans de validité pour le CA
set_var EASYRSA_CA_EXPIRE      1825
#5 ans de validité pour les certificats
set_var EASYRSA_CERT_EXPIRE    1825
```

Edit the file `openssl-easyrsa.cnf`
```bash
#File ~/EasyRSA/openssl-easyrsa.cnf
nano ~/EasyRSA/openssl-easyrsa.cnf
```
and comment the line beginning with `RANDFILE`
```bash
#RANDFILE               = $ENV::EASYRSA_PKI/.rnd
```

####Generate the CA of your VPN server
```bash
./easyrsa init-pki
./easyrsa build-ca
```
Type a passphrase to secure the CA Key. For example, you can choose passphrase `R3mot3!abz-0penVPN-CA2020`

####Edit the ~/remotelabz/.env file
You have to add your passphrase in your `.env` RemoteLabz application. In the default `.env`, you already have the following line.
```bash
SSL_CA_KEY_PASSPHRASE="R3mot3!abz-0penVPN-CA2020"
```

####Build the certificate for the VPN server
Change the value of the Common Name (CN) in the vars file of the directory EasyRSA to now create the certificate file for your OpenVPN server
```bash
cd ~/EasyRSA
#File ~/EasyRSA/vars
set_var EASYRSA_REQ_CN         "RemoteLabz-VPNServer"
```

!!! warning
    If you do not change the CN of your VPN server, you will have an error message on the client because you have generated a self-signed certificate.

Now, we can generate the certificate of your VPN Server
```bash
./easyrsa gen-req RemoteLabz-VPNServer nopass
```

Sign the CA request certificate :
```bash
./easyrsa sign-req server RemoteLabz-VPNServer
```
and you have to type the choosen passphrase of your CA (`R3mot3!abz-0penVPN-CA2020`)

Copy of the previous generated keys in OpenVPN server directory (`/etc/openvpn/server`)
```bash
sudo cp pki/issued/RemoteLabz-VPNServer.crt /etc/openvpn/server
sudo cp pki/private/RemoteLabz-VPNServer.key /etc/openvpn/server
sudo cp pki/ca.crt /etc/openvpn/server
sudo cp pki/private/ca.key /etc/openvpn/server
```

####Configure a pre-shared key to sign the data
```bash
sudo openvpn --genkey --secret ta.key
sudo cp ta.key /etc/openvpn/server
```

####Configure Diffie-Hellman
```bash
cd /etc/openvpn/server
sudo openssl dhparam -out dh2048.pem 2048
```

####Configure OpenVPN server
Edit the `/etc/openvpn/server/server.conf` file to obtain the same than the following
```bash
#File /etc/openvpn/server/server.conf
port 1194
proto udp
dev tun
ca ca.crt
cert RemoteLabz-VPNServer.crt
key RemoteLabz-VPNServer.key
dh dh2048.pem
cipher AES-256-GCM
tls-auth ta.key 0
server 10.8.0.0 255.255.255.0
keepalive 10 120
persist-key
persist-tun
status /var/log/openvpn/openvpn-status.log
log /var/log/openvpn/openvpn.log
verb 1
mute 20
explicit-exit-notify 1
duplicate-cn
push "route 10.10.10.0 255.255.255.0"
```

!!! warning
    The last line `push "route 10.10.10.0 255.255.255.0"` must be modify. You have to use your network define in your .env.local, by the two lines 
    ```BASE_NETWORK=10.0.0.0
    BASE_NETWORK_NETMASK=255.0.0.0```
    For instance, with this parameter in your .env.local, the last line must be `push "route 10.0.0.0 255.0.0.0"`
`


####Enable OpenVPN service on boot
`sudo systemctl enable openvpn-server@server`

####Start OpenVPN service
`sudo service openvpn-server@server start`

####Activate the forward between the interface
In the file `/etc/sysctl.conf`, looking for the line `#net.ipv4.ip_forward=1` and uncomment it. Then, reload this sysctl file
```bash
sudo sysctl --system
```

### Configure the mail (Exim4)
1. Configure the /etc/aliases to redirect all mail to root to an existing user of your OS
2. Check the aliases with the command `exim -brw root`
3. Edit the file `/etc/exim4/exim4.conf.template` and locate the part "Rewrite configuration" to have, for example, the following lines :
```bash
######################################################################
#                      REWRITE CONFIGURATION                         #
######################################################################

begin rewrite

user@* myemail@domain.com FfrsTtcb
root@* myemail@domain.com FfrsTtcb
```
4. Update your exim configuration with command `sudo update-exim4.conf`, following the command `sudo service exim4 restart`
5. Check all addresses are rewritten with the command `exim -brw root`

## Install RemoteLabz

The install process will create the directory `/opt/remotelabz`. You can create a link to your home with the command `sudo ln -s ~/remotelabz /opt/remotelabz`

While you're in RemoteLabz root directory :

``` bash
cd ~/remotelabz
sudo bin/install
```
The install process can take 5 minutes

##Affect the right permission to your certificate and key files for OpenVPN
The application needs to access to the certificate and key files to generate the OpenVPN file for the clients.
```bash
sudo chgrp remotelabz /etc/openvpn/server -R
sudo chmod g+rx /etc/openvpn/server -R
```


Then, you should create the `.env.local` file and put the correct environment variables from the `.env` according to your environment, including SQL database variables with `MYSQL_SERVER`, `MYSQL_USER`, `MYSQL_PASSWORD` and `MYSQL_DATABASE`.

``` bash
cd /opt/remotelabz
# To allow the web server to store the log
sudo chown -R www-data:www-data var
sudo nano .env.local
# Replace the MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE values to the right value (refer to the MySQL configuration part above)
MYSQL_USER="user"
MYSQL_PASSWORD="Mysql-Pa33wrd$"
MYSQL_DATABASE="remotelabz"
# you may change the MESSENGER_TRANSPORT_DSN variable with the following and with your credentials and server location
MESSENGER_TRANSPORT_DSN=amqp://remotelabz-amqp:password-amqp@localhost:5672/%2f/messages
```

Run the `remotelabz-ctl` configuration utility to setup your database :

```bash
sudo remotelabz-ctl reconfigure database
```

!!! info
    With the loaded fixtures, default credentials are :

    - Username : `root@localhost`
    - Password : `admin`

    You may change those values by using the web interface.

#### Generate API keys

In order for the app to work correctly, you must create a key pair for JWT. You can find detailed configuration in [the LexikJWTAuthenticationBundle doc](https://github.com/lexik/LexikJWTAuthenticationBundle/blob/master/Resources/doc/index.md#generate-the-ssh-keys).

At the root of your RemoteLabz folder:

```bash
cd /opt/remotelabz
sudo mkdir -p config/jwt
sudo openssl genpkey -out config/jwt/private.pem -aes256 -algorithm rsa -pkeyopt rsa_keygen_bits:4096
#Your can use as passphrase "JWTTok3n"
sudo openssl pkey -in config/jwt/private.pem -out config/jwt/public.pem -pubout
sudo chown -R www-data:www-data config/jwt
```

Don't forget to edit your `.env.local` :

```bash
# Replace 'yourpassphrase' by your actual passphrase
echo "JWT_PASSPHRASE=\"JWTTok3n\"" | sudo tee -a .env.local
```

!!! warning
    Avoid special character in the JWT, otherwise you will have some errors

### Configure the route from the front to the worker VM's network
We assume you have configure now all variables in your .env.local which was modified after a copy of the .env
```bash
source /opt/remotelabz/.env.local
sudo ip route add $BASE_NETWORK/$BASE_NETWORK_NETMASK via $WORKER_SERVER
```

### Instances

In order to be able to control instances on [the worker](https://gitlab.remotelabz.com/crestic/remotelabz-worker), you need to start **Symfony Messenger** :

```bash
sudo systemctl enable remotelabz
sudo systemctl start remotelabz
```

!!! warning
    When consuming messages, a timestamp is used to determine which messages the messenger worker is able to consume. Therefore, each machines needs to be time-synchronized. We recommand you to use a service like `ntp` to keep your machines synchronized.

You will also need to start the proxy service to display VNC console :

```bash
sudo npm install -g configurable-http-proxy
```

```bash
sudo systemctl enable remotelabz-proxy
sudo service remotelabz-proxy start
```

!!! warning
    Now you have to finish to install your worker before to continue

## Post configuration when RemoteLabz Worker is installed
!!! warning
    This part can only be done when you RemoteLabz application works fine. So, you have to install the Remotelabz Worker before.

### Configure the worker

### Configure your container
In the device list of the RemoteLabz, when you are connected as root, you have a device with the name "Migration". This container will be used to configure a new container, called "Service" to provide a DHCP service to each lab you will build.

First : in the sandbox, start the "Migration" device. In the console, configure the network of the device (show the log to know it) and next, type the following command :
```bash
apt-get update; apt-get -y upgrade; apt-get install -y dnsmasq;
echo "dhcp-range=RANGE_TO_DEFINED" >> /etc/dnsmasq.conf
echo "dhcp-option=3,GW_TO_DEFINED" >> /etc/dnsmasq.conf
systemctl stop systemd-resolved
systemctl disable systemd-resolved
systemctl enable dnsmasq
systemctl disable systemd-networkd
```

Your "Service" container is now ready. You have to stop the Migration device, click on Export and type, as a New Name : Service and click on the button "Export Device"
On your lab, if you add Service device, you will have a DHCP service for all your devices of your lab.

## Secure your Apache configuration (recommended)
Modify the following line in file `/etc/apache2/conf-enabled/security.conf`
```bash
ServerTokens Prod
#ServerTokens OS
#ServerTokens Full

ServerSignature Off
#ServerSignature On
```

Add these lines in file `/etc/apache2/apache2.conf`
```bash
<FilesMatch "^\.git">
        Require all denied
</FilesMatch>
```

Do not forget to restart Apache service `sudo service apache2 restart`

## Secure your server from web intrusion (recommended)
To avoid the scan url, you can use fail2ban to ban IP they scan the ssh or web access.

### On Ubuntu 20.04 LTS Server

```bash
sudo apt-get update
sudo apt-get install -y fail2ban
sudo service fail2ban restart
```

!!! warning
    This configuration can blocked your access because some request response stay in 404 when the device is not started. The following configuration is not yet recommended.

    1. At the end of the file `/etc/fail2ban/jail.conf`, add the following
    ```bash
    [apache-404]
    enabled = true
    port = http,https
    logpath = /var/log/apache2/access*.log
    #If find 3 404 errors during the findtime
    maxretry = 3
    #Ban for 1h
    bantime = 3600
    #In 600 seconds
    findtime = 600
    ```
    2. Create the file `/etc/fail2ban/filter.d/apache-404.conf` with this following content
    ```bash
    [Definition]
    failregex = ^<HOST> - .* "(GET|POST|HEAD).*HTTP.*" 404 .*$
    ignoreregex =.*(robots.txt|favicon.ico|jpg|png)
    ```
    3. Restart the fail2ban service
    ```bash
    sudo service fail2ban restart
    ```

Verify your fail2ban is up
```bash
sudo service fail2ban status
```

You will find in the log file `/var/log/fail2ban.log` all the rules you applied, banned IPs or restored access to a previously banned IP.

If you want to reinforce the security of the access to your server, you can modify the default value of fail2ban. For example, in file `/etc/fail2ban/jail.conf`, you can uncomment the following line in the [DEFAULT] section.
```bash
bantime.increment = true
```
and change the default value of `bantime` and `findtime` to 1 hour instead of 10 minutes
```bash
bantime  = 1h
findtime  = 1h
```

## Use HTTPS instead of HTTP (Optional but required if you want to use Shibboleth)
During the installation process, the file `200-remotelabz-ssl.conf` is copy in your `/etc/apache2/sites-available` directory. You have to modify the following lines to insert the right certificate files :
```bash
        SSLCertificateFile	/etc/apache2/RemoteLabz-WebServer.crt
        #SSLCertificateChainFile /etc/ssl/certs/remotelabz._INTERMEDIATE.cer
        SSLCertificateKeyFile /etc/apache2/RemoteLabz-WebServer.key
```
### Official certificate

You have just to import your certificate on your the front and on the worker

### My own certificate

To generate a self-signed certificate for your webserver, you have to follow the next steps :

```bash
cd ~/EasyRSA
cp ~/remotelabz/config/apache/cert.cnf .
```
Edit the `~/remotelabz/config/apache/cert.cnf` file and modify the value of variable `commonName` and `IP.1` with your domain and IP of your web server, respectively.
```bash
#File ~/remotelabz/config/apache/cert.cnf
[req]
default_bits  = 2048
distinguished_name = req_distinguished_name
req_extensions = req_ext
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
countryName = FR
stateOrProvinceName = Marne
localityName = Reims
organizationName = RemoteLabz
commonName = 192.168.11.131
#commonName = mydomain.com
[req_ext]
subjectAltName = @alt_names
[v3_req]
subjectAltName = @alt_names
[alt_names]
IP.1 = 192.168.11.131
```

You can now use `openssl` to generate your self-signed certificate.
```bash
cd ~/EasyRSA
openssl req -x509 -nodes -days 365 -sha512 -newkey rsa:2048 -keyout RemoteLabz-WebServer.key -out RemoteLabz-WebServer.crt -config ~/remotelabz/config/apache/cert.cnf
sudo cp /home/florent/EasyRSA/RemoteLabz-WebServer.crt /etc/apache2/
sudo cp /home/florent/EasyRSA/RemoteLabz-WebServer.key /etc/apache2/
```

You have now to activate the virtual site and the SSL module
```bash
sudo a2enmod ssl
sudo a2ensite 200-remotelabz-ssl.conf
sudo service apache2 restart
```
Verify your application is now available with HTTPS and if it works fine, you can modify the `/etc/apache2/sites-available/100-remotelabz.conf` to redirect all HTTP request to HTTPS. 
Activate the rewrite module
```bash
sudo a2enmod rewrite
```

Uncomment the following lines in the file `/etc/apache2/sites-available/100-remotelabz.conf`:
```bash
#<IfModule mod_rewrite.c>
#    RewriteEngine On
#    RewriteCond %{HTTPS} !=on
#    RewriteRule ^/?(.*) https://%{SERVER_NAME}/$1 [R,L]
#</IfModule>
```
Now, if you go to the your application's url with http, you should be redirected to HTTTS.

You can verify your certificate with the following command : 
```openssl x509 -noout -text -in RemoteLabz-WebServer.crt```

If you use only https, you need to also use WSS for all websocket connection. So, in your .env.local, you have to change the value of `REMOTELABZ_PROXY_USE_WSS=1` and copy the two files 
`home/florent/EasyRSA/RemoteLabz-WebServer.crt` and `home/florent/EasyRSA/RemoteLabz-WebServer.key` on the worker. **On the worker**, you also have to modify the `.env.local`

### Copy certificate files to the worker
We assume your `.env.local` is well configured. Change the `user` login in the following command.
```
cd /opt/remotelabz
source .env.local
scp ~/EasyRSA/RemoteLabz-WebServer.crt user@${WORKER_SERVER}:~/
scp ~/EasyRSA/RemoteLabz-WebServer.key user@${WORKER_SERVER}:~/
```


## Shibboleth (optional)

!!!warning
    You have to activate HTTPS to use Shibboleth authentication method

```bash
cd ~
curl --fail --remote-name https://pkg.switch.ch/switchaai/ubuntu/dists/focal/main/binary-all/misc/switchaai-apt-source_1.0.0~ubuntu20.04.1_all.deb
sudo apt install ./switchaai-apt-source_1.0.0~ubuntu20.04.1_all.deb
sudo apt update
sudo apt install --install-recommends shibboleth
sudo a2enconf shib
sudo a2enmod shib
sudo service apache2 restart
```

Next step, to finish to configure your Shibboleth Service Provider (SP), you have to modify your `/etc/shibboleth/shibboleth2.xml` file, following the guide from Paragraph 4, depend of your Shibboleth Identity Provider (IdP):

 - [SWITCH Shibboleth Service Provider (SP) 3.1 Configuration Guide](https://www.switch.ch/aai/guides/sp/configuration/){target=_blank}
 - [RENATER Shibboleth Service Provider (SP) Configuration Guide](https://services.renater.fr/federation/documentation/guides-installation/sp3/chap04){target=_blank}

You can find all the configuration guides on the following site :

- [On Ubuntu 20.04 LTS](https://www.switch.ch/aai/guides/sp/installation/?os=ubuntu20){target=_blank}

To enable Shibboleth site-wide, you need to change the value of `ENABLE_SHIBBOLETH` environment variable :

```bash
# .env.local
ENABLE_SHIBBOLETH=1
```