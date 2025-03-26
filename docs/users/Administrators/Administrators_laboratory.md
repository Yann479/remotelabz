# laboratory management

##basic concepts

A laboratory, also called in this documentation an activity, is an exercise associated to devices. All devices are configured to the exercise but can be reused to other activities.

##Instance management

In RemoteLabz, once a laboratory is started, the newly created instance and it's associated containers can be managed through the laboratory management panel.

![Screenshot](/images/Administrator/Administrator_Instances.png)

This panel allow to :

 - Start/Stop each containers of the lab through the start/stop button
 - have direct console access to the containers through the lab console button
 - See the startup log for each containers
 - leave the lab.Only possible when all containers are stopped.It destroy the instance completely.
 - Download the lab's associated OpenVPN file (useful to connect through protocol like SSH for instance)
 - See the lab topology through the see lab button. This will open the editor panel allowing to see the lab topology, subject and associated exercises.

!!!Warning
     Once the leave lab button has been clicked, it destroy the lab instance erasing ALL MODIFICATIONS on the lab's containers.


##Lab Topology

![Screenshot](/images/Administrator/labtopology.png)

A laboratory needs basically three elements:

 - Your own containers
 - A switch to interconnect them 
 - A service device: It is a container configured with a DHCP server that gives internet addresses to your machines.Always start it first.

You can access to the Subject and lab title through this screen as well.
 
!!!Warning
    Only teachers and administrators can create a laboratory using the "new lab" button.

##Lab edition

![Screenshot](/images/Administrator/Administrator_Lab_edition.png)

Once the laboratory has been left, an edit lab button appears which will lead you to the lab editor.
From there, you can modify every aspects of the laboratory (including it's topology, Practical subject, title...)

You can also delete the lab from there through clicking on the `delete` button.

!!!Warning
    You can't edit the lab once it has been joined.

##Lab export

It is also possible to save the lab topology on your computer.This can be accomplished through the `export` button.You can import it later using the `import lab` button on the lab's management page.

!!!Warning
    This save only the topology, but not the lab's containers !

##Lab creation
![Screenshot](/images/Administrator/Administrator_lab_creation.png)

It is possible to create a new lab on remotelabz with the `new lab` button that will appear once you get to the lab section.

You can also import a previously exported lab from there through the `import` button.
 
##Remote access.

In order to  access to your lab from your workstation (through ssh for instance), you need to connect through RemoteLabz VPN.

To do this, you need to:

1. download a client like <a href="https://openvpn.net/client/">VPNconnect</a> and then install it.
2. click on the OpenVPN file button.An .ovpn file will be downloaded.
3. double-click on the downloaded file and VPNConnect will install it automatically.
4. hit the connect button.

If the client display this, you are connected.

<img src="/images/Administrator/VPN_Connect.png" height=600px width=300px>











