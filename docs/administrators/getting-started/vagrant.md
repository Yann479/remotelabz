# Vagrant (Oracle VirtualBox)

!!! warning

    This method is deprecated since the Vagrantfile is not keep up-to-date. We're leaving it as a base to use a Vagrant VM for developpers and contributors.

This method was tested on **Windows 10** and **macOS mojave**.

## Requirements

- Vagrant (>=2)

!!! info "Recommendation"

    It is recommended to have at least 2GB of free memory to use Vagrant solution.

## Steps

```bash
git clone https://gitlab.remotelabz.com/crestic/remotelabz.git
cd remotelabz
```

In the `Vagrantfile`, modify the IP in the following line in order you to access the VirtualBox VM from your host. IP must be in the same network than your host-only network interface.

```
config.vm.network "private_network", ip: "192.168.50.4",virtualbox__intnet: true
```

Then, start the Vagrant VM :

```
sudo vagrant up
```

You can now access the website via http://localhost:8000/login.

- Username : `root@localhost`
- Password : `admin`

!!! tip

    You can also access to the created VM via ssh  

    - Username : `vagrant`
    - Password : `vagrant`

## Troubleshooting

### On Windows 10, Yarn fails to install packages while starting VM

You need to enable symlink creation on Windows 10, otherwise `yarn` won't be able to install assets to VMs `/bin`.

This can be done by executing the following steps :

Go to Run dialog by pressing ++windows+r++ and type :
```
secpol.msc
```

- Navigate to: `Local Policies > User Rights Assignment`
- Double click: `Create Symbolic Links`
- Add your `username` to the list, click `OK`
- Log off and log in again

When you log back in, you should be able to launch provision the VM without problems. If the VMs not provisioning again, destroy it before recreating it with `vagrant destroy -f`.
