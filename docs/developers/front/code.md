# Bundle
The remotelabz is divided in 4 parts :

- `remotelabz` for the frontend
- `remotelabz-worker` for the server which execute all VMs, called the backend
- `remotelabz-message-bundle` uses by both remotelabz and remotelabz-worker to manage the message exchanged between the frontend and the backend (Deprecated - replaced by RabbitMQ on recent versions)
- `network-bundle` uses by both frontend and backend (Deprecated - replaced by OpenVswitch on recent versions) 

# Certificates generation for local development

To develop on own machine, we need to build certificate to support both http and https protocols :

Generate the key for the server certificate
``` bash
openssl genrsa 2048 > server-dev-rlz-ca.key
```

Generate the CA certificate
``` bash
openssl req -new -x509 -days 365 -key server-dev-rlz-ca.key -out server-dev-rlz-ca.crt
```

Generate the key for the server certificate
``` bash
openssl genrsa 2048 > server-dev-rlz.key
```

Create the CSR
``` bash
openssl req -new -key server-dev-rlz.key -out server-dev-rlz.csr
```

Sign the certificate of the server: (do not forget to give the IP of your web server)
``` bash
openssl x509 -req -in server-dev-rlz.csr -out server-dev-rlz.crt -CA server-dev-rlz-ca.crt -CAkey server-dev-rlz-ca.key -CAcreateserial -CAserial server-dev-rlz-ca-serial.srl
```

# Code organisation
##Remotelabz
The front's code is on ```templates``` directory.

The web page of a lab is on file ```view.html.twig``` and the lab is managed by a react component ```{{ react_component('InstanceManager', {'props': props}) }}``` defined in ```assets/js/components/Instances/```

When a user starts a lab, a message (json) is sent to the worker and analyzed by ```MessageHandler/InstanceActionMessageHandler.php```. The instance, which is a started lab, is managed by the Instance Manager service in ```Service/Instance/InstanceManager.php```


# Semantic Versioning

https://semver.org/

#Dependencies

## Use of ttyd and configurable-http-proxy

We assume the following.
On the front :
```bash
configurable-http-proxy --port 8000 --api-port 8001 --log-level info --ssl-key /etc/apache2/RemoteLabz-WebServer.key --ssl-cert /etc/apache2/RemoteLabz-WebServer.crt --insecure 1 --proxy-timeout 3600 --ip 0.0.0.0 --api-ip 0.0.0.0
```
The `insecure` is used for self-signed certificate.

On the front, if you add a route to `configurable-http-proxy` with 
```bash
curl -X POST http://localhost:8001/api/routes/test12 -d '{"target":"http://192.168.11.132:35422"}'
```
on the worker, we receive a request to `/test12` So, with ttyd, we have to `ttyd -b /test12 -p 35422 command`.

If you add a route to https and use ttyd with cert, it's doesn't work.

## Yarn 

Each time you modify Javascript or ReactJS, you need to do a `yarn encore dev` All JS code is in the asset directory.

## ReactJS

Version 16.8 minimum because some script uses Hooks (https://fr.reactjs.org/docs/hooks-state.html). All codes are not translate to use Hooks.
