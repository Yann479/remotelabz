# RemoteLabz's front update guide

###Save your .env file
All configuration variables are saved in the file `.env.local` or if you don't have this file, in the file `.env`
If you don't have a .env.local, save your .env to .env.local
```bash
sudo -u remotelabz cp .env .env.local
```
Check your server.conf of your openvpn. Some deprecated parameters can be replaced.

###Update the code
```bash
cd /opt/remotelabz
git fetch
git pull
```

!!! info
    To choose a specific version :
    ```bash
    git checkout tags/2.X.Y
    ```
    or a branch
    ```bash
    git checkout dev
    ```

Compare your `.env.local` file with the `.env` file to make sure the same parameters are there

```bash
sudo composer update
sudo yarn encore prod
sudo php bin/console doctrine:migrations:migrate
sudo php bin/console cache:clear
sudo chown remotelabz:www-data * -R
sudo chmod g+w /opt/remotelabz/var -R
sudo chmod g+w /opt/remotelabz/public/uploads -R
sudo chmod g+r config/jwt/private.pem
sudo systemctl daemon-reload
sudo service remotelabz restart
```

##Migration from 2.4.3 to 2.4.4

The RabbitMQ configuration need to be modified in order to manage multiples workers.
```bash
sudo rabbitmqctl set_user_tags remotelabz-amqp administrator
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmqadmin delete exchange name=worker
```

Then, the following commands must be entered  :
```bash
cd /opt/remotelabz;
sudo chmod 664 config/packages/messenger.yaml;
sudo chown www-data:www-data config/templates;
sudo chmod 664 config/templates;
sudo mkdir backups;
sudo chmod 644 backups;
sudo apt-get update;
sudo apt-get install tmux;
```

!!! warning
    Prior to execute the following task, update all your workers. Their version must not be older than 2.4.3 or dev from october 26, 2024 (commit 5b929ae)

Check that you have a `remotelabz` user with a directory `/home/remotelabz` and `/home/remotelabz/.ssh` with the correct ownerships and permissions.

Generate the key named `myremotelabzfront`, defined in your `.env.local` with the following command:

```bash
sudo -u remotelabz ssh-keygen
sudo -u remotelabz ssh-keygen -m PEM -t rsa -f /home/remotelabz/.ssh/myremotelabzfront
sudo -u remotelabz ssh-copy-id -i /home/remotelabz/.ssh/myremotelabzfront.pub remotelabz-worker@Worker_X-IP
```

Update your file  `/etc/sudoers.d/remotelabz`

```bash
sudo cp /opt/remotelabz/config/system/sudoers /etc/sudoers.d/remotelabz
```

##Migration from 2.4.1.5 to 2.4.2.4
A new feature has been introduced which allow to define which protocol that can be used to access the device's console : `vnc`, `serial` or `login`. So we have to add this protocol to each device. You can have more than one procotol to the same device. For example, we can use the vnc protocol to connect to a qemu vm and the serial protocol to use telnet on the serial line of the VM where the OS is configured.

The main usage is : 
  - `vnc` for qemu VM
  - `login` for container lxc
  - `serial` for network device like firewalls, switchs, routers, ...

##Migration from 2.4.1.1 to 2.4.1.3
In your device, you have a device which is named "Migration". This container will be used to configure a new container, called "Service" which will provide a DHCP service to each lab you will build.

First : in the sandbox, start the "Migration" device. In the console, configure the network of the device (show the log to know it) and next, type the following command :
```bash
apt-get update; apt-get -y upgrade; apt-get install -y dnsmasq;
echo "dhcp-range=RANGE_TO_DEFINED" >> /etc/dnsmasq.conf;
echo "dhcp-option=3,GW_TO_DEFINED" >> /etc/dnsmasq.conf;
sync;
systemctl enable dnsmasq;
```
Modify your /etc/sudoers file to add, at the end, the following lines: 
```bash
Cmnd_Alias REMOTELABZ_CMDS = /bin/systemctl start remotelabz*, /bin/systemctl stop remotelabz*, /bin/systemctl status remotelabz*

%www-data ALL=(ALL) NOPASSWD: REMOTELABZ_CMDS
```

##Migration from 2.4.0 to 2.4.1.1

To update from 2.4.0 to 2.4.1.1, on the worker, you need to type the following command :
```bash
sudo lxc-create -t download -n Migration -- -d debian -r bullseye -a amd64 --keyserver hkp://keyserver.ubuntu.com
```
Then,create a new device like in the following image :
![Screenshot](/images/Migration/Migration.jpg)
In the Device Sandbox menu, click on the button "Modify" of the device "Migration" and start it (with button play). On the worker, a new container is created and started with an uuid name. You can find the uuid under the device name "Migration", like in the following image.
![Screenshot](/images/Migration/Migration-Sandbox.jpg)
In this example, the uuid is`a18d566a-6023-43df-a16e-4367065c5ecf`.This container can be listed directly on the worker, using the command `lxc-ls -f`.
![Screenshot](/images/Migration/Migration-Console.jpg)

A DHCP server must be installed on this container. The example below is using the previous uuid.
```bash
sudo lxc-attach -n "a18d566a-6023-43df-a16e-4367065c5ecf"
echo "nameserver 1.1.1.3" > /etc/resolv.conf
apt-get update
apt-get upgrade
apt-get install dnsmasq
echo "dhcp-range=RANGE_TO_DEFINED" >> /etc/dnsmasq.conf
```
Once done, stop the modified container from the RemoteLabz interface and export it using the name "Service".
![Screenshot](/images/Migration/Migration-Export.jpg)

Then a new operating system and device is created with the name "Service" but the name of the operating system's image is wrong. It is called "service_" following a date.Using the Edit button, Edit this name and name it "Service" instead. 
![Screenshot](/images/Migration/Migration-OS-image.jpg)

Change the image filename "service_" to "Service"
![Screenshot](/images/Migration/Migration-OS-changed.jpg)

Now, once a new lab has been created using this device, all other devices on it will automatically receive IPv4 addresses thanks to the DHCP server installed in the associated container. The DHCP's IPV4 will be the (last IPv4 - 1). The last IP always corresponds to your laboratory's gateway.

![Screenshot](/images/Migration/Migration-End.jpg)


##Migration from 2.3 to 2.4.0
To update from 2.3 to 2.4.0, add default image to all labs with the following command :
```bash
sudo find /opt/remotelabz/public/uploads/lab/banner/* -type d -exec cp /opt/remotelabz/public/build/images/logo/nopic.jpg {}/nopic.jpg \;
```
If needed, add all user in the default group so they can access to the labs.


