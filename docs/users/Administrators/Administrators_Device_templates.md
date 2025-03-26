#Device template management
From this area, you can manage every existing device templates.
![Screenshot](/images/Administrator/Device_templates/Device_Template_overview.png)
A device template is a model from which a lab device is created.It includes various parameters like:

* Name : name of the template
* Brand : Brand of the device.
* Model : Model of the device.
* Type : Nature of the device (Virtual machine, container ...)
* Hypervisor : Correspond to the hypervisor the device will run on (can be qemu,lxc or natif).
* Operating System : correspond to the device's Operating System.
* Flavor : The memory profile it will use (control the amount of allocated RAM and disk) 
* Nb CPU : number of CPU
* Nb Core : number of core per CPU
* Nb Socket : number of CPU Socket
* Nb Threads : number of threads per CPU
* Network Interfaces: number of network interfaces (limited to 19)
* Control protocol types : control protocol used to administrate the device.
* Template: allow or disallow use in the lab editor.

#Device template creation
Once you've clicked on the `new Device` button, you will be brought to a new screen.
![Screenshot](/images/Administrator/Device_templates/Device_Template_add.png)
Once you've finished adding your parameters, click on `submit` to add your new device template.

#Device template edition
Once selected, you can also edit the Device's name through the `edit` button or delete it through the `Delete` button.
![Screenshot](/images/Administrator/Device_templates/Device_Template_selected.png)
Once you have pressed the `edit` button,you will be able to edit the Device through this screen
![Screenshot](/images/Administrator/Device_templates/Device_Template_edited.png) 
Then click on the submit button to validate your changes and modify the selected device accordingly.
