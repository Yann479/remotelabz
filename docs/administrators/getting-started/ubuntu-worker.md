# RemoteLabz's Worker installation guide

This section guides you through the installation of RemoteLabz's worker and its components on an Ubuntu system. We assume you have already installed an Ubuntu Server 20.04 LTS.

!!! note "Foreword"

    - This section has only been tested with **Ubuntu Server 20.04 LTS**

# Retrieve the RemoteLabz source
A remotelabz directory will be create on your home directory.
```bash
cd ~
git clone https://github.com/remotelabz/remotelabz-worker.git
cd remotelabz-worker
```

!!! warning
    If you want to install only a specific version, you have to do the following instruction, for version 2.4.1 for example.
    ```bash    
    git clone https://github.com/remotelabz/remotelabz-worker.git --branch 2.4.1 --single-branch
    ```
    ou
    ```bash    
    git clone https://github.com/remotelabz/remotelabz-worker.git --branch dev
    ```

# Installation
You should modify the `.env` file according to your environment

``` bash
nano .env
# you may change the network interface name
# DATA_INTERFACE will be used by the virtual machine
# ADM_INTERFACE will be used by the RemoteLabz's front and the RabbitMQ to communicate with the worker. This interface is also used to ssh connexion
DATA_INTERFACE="enpX"
ADM_INTERFACE="enpY"
#The DATA_INTERFACE will be bridge, during the install phase, with the br-worker-data interface (which will be an OVS)
#Must be equal to the BASE_NETWORK of your .env.local on your front
LAB_NETWORK=10.0.0.0/8

# you may change the MESSENGER_TRANSPORT_DSN variable with the following, with your credentials, and the RabbitMQ IP or its FQDN. If the RabbitMQ is on your front, you have to use the adm network 
MESSENGER_TRANSPORT_DSN=amqp://remotelabz-amqp:password-amqp@X.X.X.X:5672/%2f/messages
#Must be equal to the value of the parameter server in your /etc/openvpn/server/server.conf on your Front
VPN_NETWORK=X.X.X.X
VPN_NETWORK_NETMASK=255.255.255.0
#The FRONT_DATA must be equal to the IP of the PUBLIC_ADDRESS parameter of the .env.local from the Front 
FRONT_DATA_IP=Y.Y.Y.Y
```
Next, type 
```bash
sudo ./install
```
# Configuration
### Configure WSS
If you have configured the front with HTTPS, you have to copy your certificate to the `/opt/remotelabz-worker/config/certs/` directory, regarding the two parameters in your .env.local
`REMOTELABZ_PROXY_SSL_KEY` and `REMOTELABZ_PROXY_SSL_CERT`

!!! warning
    You need to use the same certificate between your front and this worker. Don't forget to copy them and to change it automatically when your certificate expired.

### Internet access (From Version 2.3.0 and before 2.4.0)
For testing the Internet access on RemoteLabz Version 2.3.0 to 2.4.0, you have to enable the NAT with the command
```bash
sudo iptables -t nat -A POSTROUTING -o $ADM_INTERFACE -s $LAB_NETWORK -j MASQUERADE
```
From version 2.4.0, this command is executed with the remotelabz-worker service. The admin network interface is used to nat the network because we assume the admin network is connected to Internet. For security reason, we recommand to use the data network to route and nat the data VM. So, your data network need to be connect to internet.

In the next version (2.5.0), Internet connection will be configurable from the graphical interface and the NAT will be like that :
```bash
sudo iptables -t nat -A POSTROUTING -o $BRIDGE_INT -s $LAB_NETWORK -j MASQUERADE
```

### Instances
```bash
sudo service remotelabz-worker start
```

You can check the log of the worker in `~/remotelabz-worker/var/log/prod.log`

## Options

- `-p` Port used by remotelabz-worker
    - Default : `8080`

!!! warning
    When consuming messages, a timestamp is used to determine which messages the messenger worker is able to consume. Therefore, each machines needs to be time-synchronized. We recommand you to use a service like `ntp` to keep your machines synchronized.

## Configure your logrotate
Add the following file `/etc/logrotate.d/remotelabz-worker`

```bash
/opt/remotelabz-worker/var/log/*.log {
        daily
        missingok
        rotate 52
        size 100M
        compress
        notifempty
        create 664 remotelabz-worker www-data
        su remotelabz-worker www-data
}
```
## In progress (in next version 2.4.1) - documentation of this part in the front
To install and test a service container :
Last Debian stable (16 Nov. 2021) Linux Install
```
sudo lxc-create -t download -n Container_Name -- -d debian -r bullseye -a amd64 --keyserver hkp://keyserver.ubuntu.com
```
Edit the config of the container:
```
sudo nano /var/lib/lxc/Container_Name/config
```

