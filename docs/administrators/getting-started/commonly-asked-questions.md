# Commonly Asked Questions

## RemoteLabz Logs location 

RemoteLabz's logs are located under `/opt/remotelabz/var/log/` and RabbitMQ's log under `/var/log/rabbitmq`

## Change password of phpmyadmin
```bash
sudo mysql -h localhost -u root -p
CREATE USER 'phpmyadmin'@'localhost' IDENTIFIED BY '<New-Password-Here>';
GRANT ALL PRIVILEGES ON *.* TO 'phpmyadmin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
If you have finish with your modification, you have to go lab and delete the new lab created from the sandbox.

## List the RabbitMQ messages waiting
On the RabbitMQ server
To list the number of message in each queues
```bash
sudo rabbitmqctl list_queues
```

## How to modify the image of the device
To avoid a teacher or an user include a corrupted image, only the administrator can modify an existing default image. With the menu `Device Sandbox`, a new lab is created and after the export button is click, a new device template and new Operating Systems are created. To make an export, you have to :

1. Click on `Device Sandbox`
2. Click on the Modify button of the device whose image you wants to modify
3. Start the device
4. Make your modification
5. Stopped the device
6. Click on Export and choose a name for you new device template
7. Leave the lab

## How to increase size of disk on LVM virtual machines
1. Shutdown the VM
2. Right click the VM and select Edit Settings
3. Select the hard disk you would like to extend
4. On the right side, make the provisioned size as large as you need it and confirm
5. Power on the VM and connect to it.
6. Identify your disk name with `sudo fdisk -l` for example /dev/sda
7. `sudo fdisk /dev/sda`
8. Enter `p` to print the partition table
9. Enter `n` to add a new partition
10. Enter `p` again to make it a primary partition
11. Enter the number of your new partition
12. Pick the first cylinder which will most like come at the end of the last partition (this is the default value)
13. Enter the amount of space (default is the rest of space available)
14. Enter `w` to save these changes
15. Restart the VM and log in
16. Type `sudo fdisk -l` and check that a new partition is present
17. Find your volume group with `df -h`.
    * Example: `/dev/mapper/ubuntu--vg-root 15G 4.5G ...`
    * Volume group is: `ubuntu-vg`
18. Extend the volume group : `sudo vgextend [volume group] /dev/sdaX`
    * Example: `sudo vgextend ubuntu-vg /dev/sda3`
19. Find the amount of free space available : `sudo vgdisplay [volume group] | grep "Free"`
20. Expand the logical volume : `sudo lvextend -L+[freespace]G /dev/[volgroup]/[volume]`
     * Example 1: `sudo lvextend -L+64G /dev/ubuntu-vg/root`
     * Example 2: `sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu`
21. Expand the ext3 file system in the logical volume : `sudo resize2fs /dev/[volgroup]/[volume]`
     * Example: `sudo resize2fs /dev/ubuntu-vg/root`
22. You can now run the df command to very that you have more space `df -h`

## How to import a new image from an OVA
We assume your image has the name `import_vm.ova` in OVF format and in your home directory.
```bash
cd ~
mkdir new_image
cd new_image
tar xvf ../import_vm.ova 
qemu-img convert import_vm.vmdk new_image.img -O qcow2
sudo mv new_image.img /opt/remotelabz-worker/images/
```
As root, in operating system (OS), add a new operating system and in the Image filename parameter, give the name of your new image file. For our example, you have to type "new_image.img". Finally, create a new device which use this OS.

## How to remove all bridge OVS on a worker manually
```bash
for i in $(sudo ovs-vsctl show | grep "Bridge" | grep "br-" | cut -d " " -f 6); do sudo ovs-vsctl del-br $i; done;
```

## How to check the queue and exchange with RabbitMQ
To list the queues
```bash
rabbitmqadmin list queues
```

To list the exchange
```bash
rabbitmqadmin list exchanges
```

To delete an exchange
```bash
sudo rabbitmqadmin delete exchange name="worker"
```

To create an exchange with a specific type (direct or fanout)
```bash
sudo rabbitmqadmin declare exchange name="worker" type="direct"
```

To clear a queue
```bash
sudo rabbitmqadmin purge_queue queue_name
```


## How to list all routes of the proxy
On the front
```bash
curl http://localhost:8001/api/routes
```


## Too many file opened
Many parameters have to be modify. Add following lines in `/etc/sysctl.conf` and execute a `sysctl -p` the system read this file.

```bash 
fs.inotify.max_user_watches=60000
fs.inotify.max_user_instances=10000
fs.file-max=9793398
```

You can also modify the file `/etc/security/limits.conf` which is read on boot and use the command `prlimit --nofile=300000:500000 --pid Process_Number` (`ulimit` is obsolete) to change this value for a given process
without reboot your server

```bash
*               soft    nofile          65535
*               hard    nofile          524288
```

## How to install with iso on CD and driver on floppy

```bash
qemu-system-x86_64 -enable-kvm -machine accel=kvm:tcg -cpu max -display none -name Your_VM -m 1024 -drive file=/path/file.img,if=virtio -smp 1 -device e1000,netdev=eth0-4f5965f2,mac=52:54:00:9E:92:56 -netdev tap,ifname=eth0-4f5965f2,id=eth0-4f5965f2,script=no -k fr -rtc base=localtime,clock=host -vga qxl -usb -device usb-tablet,bus=usb-bus.0 -device usb-ehci,id=ehci -vnc 0.0.0.0:31338 -boot d -blockdev driver=file,node-name=f0,filename=/path/virtio-win.vfd -device floppy,drive=f0 -cdrom filename.iso
```
