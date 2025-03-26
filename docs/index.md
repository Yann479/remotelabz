[RemoteLabz](https://remotelabz.com){:target="_blank"}
==========

[RemoteLabz](https://remotelabz.com){:target="_blank"} is an educational application aimed at helping students and teacher during practical work.

It allow Teachers to create various exercises (like developing and testing computer code, looking for vulnerabilities in a network...) based on different network topologies and manage their students while performing them.

 Student have the freedom to experiment and learn from everywhere, without harming their computer or network.
 
 Each time a student finishes his works, all the virtual environment he used is destroyed ,thus eliminating any waste of computer resources.

## History    

The first version, created in 2009, was coded in J2EE, allowing taking control of physical equipments. For security reasons, the J2EE version is no longer in use . However some of it's tools are still used today.

In 2017, a 2nd version was completely rewritten aiming to comply to actual IT training requirements such as having the possibility to carry out practical work in a pre-configured environment and without risking any damages to the user's personal computer or network resources.

## General informations

RemoteLabz consists of three software components :
 
- The front web site, called the RemoteLabz's front.
- The backend server which execute the virtuals machines, called *remotelabz-worker*.
- The broker service (RabbitMQ) which will manage communication between the front and the workers.

!!! info
    Technically, You can have all these components running in a single host, but since remotelabz-worker has to run an hypervisor (QEMU) which may consume a lot of resources. It is best to use a different server for each components.
   

The front is the only host which may require direct Internet access.In this case, extra attention must be paid regarding the security of the host it's running on.
For instance, it is highly recommended to install a [fail2ban](https://github.com/fail2ban/fail2ban) service and securing any remote access service like SSH using certificates or strong passwords.

## Physical Network Topology

![network_architecture](/images/RemoteLabz-Ports.png)


!!! example "Ports used (Summary)"

    === "Internet to RemoteLabz"
        - **TCP 80 (443)** : HTTP(S) pages
        - **TCP 8000** : WebSocket
        - **UDP 1194** : OpenVPN

    === "RemoteLabz to RemoteLabz-Worker"
        - **TCP 8080** : Remotelabz-Worker Internal API

    === "RemoteLabz Worker to RabbitMQ"
        - **TCP 5672** : AMQP


