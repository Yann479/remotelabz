# Troubleshooting

## 500 Internal Server Error on Login page
Wrong permission for config/jwt/
```bash
# Change owner of config/jwt/*
chown -R www-data:www-data config/jwt
```

## 500 Internal Server Error on Labs page
Wrong permission in var/cache/prod/
```bash
# Change owner of cache/prod/
chown -R www-data:www-data *
```

## Error in prod when update
If an error occurred when you update your version, from prod or older version, you can :

 - delete the `*.lock` file
 - check with `git status` if you have additional file on your filesystem and delete them
 - delete the `var/cache` directory

## No device templates are displayed on editor
If you want to add a device in the editor and no templates are displayed in the dropdown, you have to change the permission of config/templates:
```bash
chown www-data:www-data config/templates
chmod 664 config/templates
```

## Error with numpy when installing

If the setup fails while processing numpy-2.1.3.tar.gz with this error:
    
`error: Couldn't find a setup script in /tmp/easy_install-cw60uo3_/numpy-2.1.3.tar.gz
ERROR: (`
    
 Install numpy manually with `pip install numpy.` and re-run the installation script.
    
## lxc error while creating alpine 3.15 when installing

This is due to the script asking to install a version of Alpine that is no longer maintained.
To circumvent this, the install script must be modified.
Open the install script and change those lines

```bash
LXC=`lxc-ls -name "Alpine3.15"`;
if [ "${LXC}" == "" ] ; then
echo "Creation of a container Alpine 3.15"
DOWNLOAD_KEYSERVER="keyserver.ubuntu.com" lxc-create -t download -n Alpine3.15 -- -d alpine -r 3.15 -a amd64
echo "No default login, please use Sandbox to configure a new OS from this" >> "/var/lib/lxc/Alpine3.15/rootfs/etc/issue"
echo "nameserver 1.1.1.3" > "/var/lib/lxc/Alpine3.15/rootfs/etc/resolv.conf"
echo "OK ✔️"
fi;    
```
to

```bash
LXC=`lxc-ls -name "Alpine3.17"`;
if [ "${LXC}" == "" ] ; then
echo "Creation of a container Alpine 3.17"
DOWNLOAD_KEYSERVER="keyserver.ubuntu.com" lxc-create -t download -n Alpine3.17 -- -d alpine -r 3.17 -a amd64
echo "No default login, please use Sandbox to configure a new OS from this" >> "/var/lib/lxc/Alpine3.17/rootfs/etc/issue"
echo "nameserver 1.1.1.3" > "/var/lib/lxc/Alpine3.17/rootfs/etc/resolv.conf"
echo "OK ✔️"
fi;
```

This will force the installer to install a version of Alpine that is still maintained (3.17).
Re-run the install script after this.


 






    


