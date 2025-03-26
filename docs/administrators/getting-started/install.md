# Installation
## General informations
RemoteLabz needs at least 2 hosts :
 
- 1 for the web site, called the RemoteLabz's front.
- 1 for the server which execute the virtuals machines, called *remotelabz-worker*.
- (Optionnal) 1 for the RabbitMQ which can be also a virtual machine.

!!! info
    Technically, you may be able to use only one host for all services, but since remotelabz-worker has to run QEMU, we recommend to use a different server for each service.

The front can be a virtual machine and it will be the only host with an access from Internet. So, you have to secure your ssh service with the lastest recommandation and we recommand you to install a [fail2ban](https://github.com/fail2ban/fail2ban) service for example.

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

## Logs

RemoteLabz's logs are located under `/opt/remotelabz/var/log/` and RabbitMQ's log under `/var/log/rabbitmq`
