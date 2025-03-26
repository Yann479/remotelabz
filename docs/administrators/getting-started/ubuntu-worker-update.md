# RemoteLabz's worker update guide

###Save your .env file
All configuration variables are saved in the file `.env.local` or if you don't have this file, in the file `.env`
If you don't have a .env.local, save your .env to .env.local
```bash
sudo -u remotelabz cp .env .env.local
```

###Update the code
```bash
cd /opt/remotelabz-worker
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

Compare your `.env.local` file with the `.env` file to be sure the same parameters are set 

```bash
sudo composer update
sudo php bin/console cache:clear
sudo chown remotelabz-worker:www-data * -R
sudo chmod g+w /opt/remotelabz-worker/var -R
sudo systemctl daemon-reload
sudo service remotelabz-worker restart
```

## From 2.4.2.6 and above to version 2.4.3
When you link a worker to the front, don't forget to add the following lines on the `/opt/remotelabz-worker/config/packages/messenger.yaml` file, in the part 
```bash
framework:
    messenger:
        transports:
            async: '%env(MESSENGER_TRANSPORT_DSN)%'
            worker: 
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                options:
```
On your first worker Worker_1

```bash
queues:
    messages_worker1:
        binding_keys: [Worker_1-IP]
```

On your second worker Worker_2
```bash
queues:
    messages_worker2:
        binding_keys: [Worker_2-IP]
```
And so on, for all your workers

Then, you will have to define the authentication key between all workers for ssh. On each worker, you have to execute the following commands. 

!!! warning
    Obviously, for the following command, you need to remember the password of your `remotelabz-worker` user on each worker. If not already done, you need to define it first using `sudo passwd remotelabz-worker`. All workers must have the same password.

```bash
sudo mkdir /home/remotelabz-worker
sudo mkdir /home/remotelabz-worker/.ssh
sudo chown remotelabz-worker:remotelabz-worker /home/remotelabz-worker/.ssh
sudo chmod 700 /home/remotelabz-worker/.ssh
sudo -u remotelabz-worker ssh-keygen -m PEM -t rsa -f /home/remotelabz-worker/.ssh/myremotelabzkey
sudo chown remotelabz-worker:remotelabz-worker /home/remotelabz-worker/.ssh -R
sudo chmod 600 /home/remotelabz-worker/.ssh/myremotelabzkey
```

Once done, for each RemoteLabz-Worker, you have to execute the following command to allow each worker to connect, using it's own key, to another one.
```bash
sudo -u remotelabz-worker ssh-copy-id -i /home/remotelabz-worker/.ssh/myremotelabzkey.pub remotelabz-worker@Worker_X-IP
```

To test the ssh key copy, you have to :
```bash
sudo -u remotelabz-worker ssh -i /home/remotelabz-worker/.ssh/myremotelabzkey remotelabz-worker@Worker_X-IP
```

The package php-ssh2 on the front is also required, you can install it using the command below :
```bash
sudo apt-get install php-ssh2
```


Last, update your sudo file :
```bash
sudo cp /opt/remotelabz-worker/config/sudo/remotelabz-worker  /etc/sudoers.d/remotelabz-worker
```

## From 2.4.1.2 and above Version 2.4.1.3

First,you have to Install the ttyd package

```bash
sudo apt-get install -y screen build-essential cmake git libjson-c-dev libwebsockets-dev
cd ~
git clone https://github.com/tsl0922/ttyd.git
cd ttyd && mkdir build && cd build
cmake ..
make && sudo make install
```

Then, You need to install some default container
```bash
sudo lxc-create -t download -n Migration -- -d debian -r bullseye -a amd64 --keyserver hkp://keyserver.ubuntu.com;
sudo lxc-create -t download -n Debian -- -d debian -r bullseye -a amd64 --keyserver hkp://keyserver.ubuntu.com;
sudo lxc-create -t download -n Ubuntu20LTS -- -d ubuntu -r focal -a amd64 --keyserver hkp://keyserver.ubuntu.com;
sudo lxc-create -t download -n Alpine3.17 -- -d alpine -r 3.17 -a amd64 --keyserver hkp://keyserver.ubuntu.com;
sudo su;
echo "nameserver 1.1.1.3" > "/var/lib/lxc/Migration/rootfs/etc/resolv.conf";
echo "nameserver 1.1.1.3" > "/var/lib/lxc/Debian/rootfs/etc/resolv.conf";
echo "No default login, please use Sandbox to configure a new OS from this" >> "/var/lib/lxc/Debian/rootfs/etc/issue";
echo "No default login, please use Sandbox to configure a new OS from this" >> "/var/lib/lxc/Ubuntu20LTS/rootfs/etc/issue";
echo "No default login, please use Sandbox to configure a new OS from this" >> "/var/lib/lxc/Alpine3.15/rootfs/etc/issue";
echo "nameserver 1.1.1.3" > "/var/lib/lxc/Alpine3.15/rootfs/etc/resolv.conf";
exit;
```
Once done, you have to restart all the workers.
```bash
echo "%remotelabz-worker     ALL = (ALL) NOPASSWD: $(which ip), $(which iptables), $(which ovs-vsctl), $(which systemctl) start remotelabz*, $(which systemctl) stop remotelabz*, $(which systemctl) restart remotelabz*, $(which systemctl) status remotelabz*" | sudo tee /etc/sudoers.d/remotelabz-worker
echo "%www-data     ALL = (ALL) NOPASSWD: $(which ip), $(which iptables), $(which ovs-vsctl), $(which systemctl) start remotelabz*, $(which systemctl) stop remotelabz*, $(which systemctl) restart remotelabz*, $(which systemctl) status remotelabz*" | sudo tee -a /etc/sudoers.d/remotelabz-worker
echo "net.ipv6.route.max_size = 20000" | sudo tee -a /etc/sysctl.conf
```
