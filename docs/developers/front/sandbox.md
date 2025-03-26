# Devices Sandbox and Export

The goal of the sandbox is to modify an existing VMs images on the RemoteLabz and then create a new **Device** and **Operating System** templates.

## How to access
When you click on the menu ```Device Sandbox``, the route `/admin/devices_sandbox` is used. This function is only authorized to a user with an admin role.<br>
This page is managed by [DeviceSandboxController](https://github.com/remotelabz/remotelabz/blob/master/src/Controller/DeviceSandboxController.php).<br>
It retrieves all existing device templates in the system and pass it to the template to format the data. It also pass **User** information in the props for later<br>
The view is described in [templates/device_sandbox/index.html.twig](https://github.com/remotelabz/remotelabz/blob/master/templates/device_sandbox/index.html.twig).

The data are processed in React Component that are defined in [assets/js/components/Sandbox/*](https://github.com/remotelabz/remotelabz/tree/master/assets/js/components/Sandbox)<br>

## Sandbox Lab
In order to launch a Device we need to have it in a **Lab**. So if we want to modify an existing image (**Device**) we need to create a **Lab** and then add the **Device** that we want to modify.<br>
All the process in order to achieve this is done in the React Component [SandboxListItem](https://github.com/remotelabz/remotelabz/blob/master/assets/js/components/Sandbox/SandboxListItem.js) and is made by calling the API.

When you click on ``Device Sandbox``, the process follows the steps :

- listing all existing labs
- if you click on button ``Modify``, a new lab is created with the name : ``Sandbox_user.uuid_device.id``
- you have to start the device to modify it in this new lab. As soon as you starts the device, a new image is created on the worker filesystem
- when you have finish to modify your device, you can stop it and click on the ``Export`` button
- after type a name to your new device in the text area ``new name``, when you will click on ``Export Device`` button, a new image will be created on the worker filesystem with the name typed in the text area. It creates also a new Operating system and new Device template.
- you have to stop the lab and delete it if you have finish with your modification.

### Creating Lab
First we create a new **Lab** with a call to the API and we get his object in return
``` javascript
await this.api.post("/api/labs").then(response => {
    lab = response.data
});
```
We wait the response of the API to continue. <br>
Now we want to name our new **Lab** with an identifiable name in order to retrieve it later. The name will look like "Sandbox_USER-UUID_DEVICE-ID"<br>
``` javascript
var labName = "Sandbox_" + this.props.user.uuid + "_" + device.id;
var labObj = { id: lab.id, fields: {name: labName}};
Remotelabz.labs.update(labObj);
```

### Adding Device to Lab
When we call the API to add a **Device** to a **Lab**, it clone the **Device** passed and then add the clone to the **Lab**.
The **Device** object passed contains the full definition of the **Device** and of its other attached entities like **Flavor**, **OperatingSystem** and **NetworkInterfaces**.
In order to be compliant with the **Device** form the API we need to make somes changes to our actual **Device** and replace entities by their id.<br>
After that we can push the **Device** to the **Lab** and wait that it process to continue.
``` javascript
device.flavor = device.flavor.id;
device.operatingSystem = device.operatingSystem.id;
device.isTemplate = false;
device.networkInterfaces.forEach(element => networkInterfaces.push(element.id));
device.networkInterfaces = networkInterfaces
await this.api.post('/api/labs/' + lab.id + '/devices', device);
```

### Creating and starting LabInstance
Now that we got our **Lab** we need to create and start an instance of it in order to start the **Device**.
We call the API to create and start it with the **User** as **Instancier**
``` javascript
Remotelabz.instances.lab.create(lab.uuid, this.props.user.uuid, 'user');
```

### Accessing the Lab
After this process, we can set the state 'exist' of the sandbox lab to 'true' to make the button 'Redirect' appears instead of 'Modify'.
It will redirect the **User** to `/admin/devices_sandbox/{lab-id}`

## Sandbox Lab view page
It takes the template of a **Lab** view page and we adjust it by removing not neccessary data (like Lab name, view_as options). Template can be found here [templates/device_sandbox/view.html.twig](https://github.com/remotelabz/remotelabz/blob/master/templates/device_sandbox/view.html.twig)

### Export button
In this part, all the code is in [InstanceListItem.js](https://github.com/remotelabz/remotelabz/blob/master/assets/js/components/Instances/InstanceListItem.js)
We want to export VMs so we need to add an export button with a text option (to name the new **Device**). <br>
We only want to export the VM if it's stopped and come from a Sandbox Lab. The first button will toggle the form.
``` javascript
{(deviceInstance.state == 'stopped' && this.props.isSandbox) &&
    <div onClick={() => this.toggleShowExport()}>
    {this.state.showExport ?
        <Button variant="default"><SVG name="chevron-down"></SVG> Export</Button>
        :
        <Button variant="default"><SVG name="chevron-right"></SVG> Export</Button>
    }
    </div>
}
...
toggleShowExport = () => {
    this.setState({ showExport: !this.state.showExport });
}
```
When the button is pressed, it will show a form that is managed by the React Component [InstanceExport](https://github.com/remotelabz/remotelabz/blob/master/assets/js/components/Instances/InstanceExport.js).
We pass to the Component the actual deviceInstance that we want to export and the function that manage the exportation process.
``` javascript
{(deviceInstance.state == 'stopped' && this.state.showExport) &&
    <InstanceExport deviceInstance={deviceInstance} exportDeviceTemplate={this.exportDeviceTemplate} />
}
```
The function ***exportDeviceTemplate*** is making a call to the API endpoint `/api/instances/export/by-uuid/` with the deviceInstance uuid and the new name of the new template.

## Export Process
### RemoteLabz
In order to export a **Device**, we need to make an API endpoint that is managed in [InstanceController](https://github.com/remotelabz/remotelabz/blob/master/src/Controller/InstanceController.php#L152). It requires the deviceInstance UUID, to fetch the Object from the database, and a name.
After that we can launch the process to create a clone of the **Device** and its **Operating System**.<br>
The process is managed in [InstanceManager](https://github.com/remotelabz/remotelabz/blob/master/src/Service/Instance/InstanceManager.php#L211) by the function ***export***.<br>
In order to avoid conflicts in image name, we need to make it unique by adding current date and time plus an id.
```php
now = new DateTime();
$imageName = transliterator_transliterate('Any-Latin; Latin-ASCII; [^A-Za-z0-9_] remove; Lower()', $name);
$id = uniqid();
$imageName .= '_' . $now->format('Y-m-d-H:i:s') . '_' . substr($id, strlen($id) -3, strlen($id) -1) . '.img';
```
Now that we got our unique image name we can send to the Remotelabz-Worker an export message with the labInstance and the new image name as data.<br><br>
Next step is to clone the Device and its Operating System data. First we create a new **OperatingSystem** object with the name chosen by the User and the image name created just before.
Then, we create a new **Device** object and copy data from the old **Device** except his name and **OperatingSystem**.
After that, we can link the **OperatingSystem** to its new **Device** and apply changes in the database.

- ### RemoteLabz-Worker
Currently, the VMs are managed with QEMU. When a **Device** instance is created, it create a snapshot of the base image and save it into `./instances/{group|user}/{groupUUID|userUUID}/{labInstanceUUID}/{deviceUUID}/`.<br>
In order to commit changes done in the SandboxLab **Device** we need to rebase the base image with this snapshot, but to not corrupt others snapshots that could exist we are going to apply this to a copy of the base image.
This is done in [InstanceManager.php](https://github.com/remotelabz/remotelabz-worker/blob/master/src/Service/Instance/InstanceManager.php#L624) in the ***exportDeviceInstance*** function.
>> The following commands are the 'template' command executed in the function
```bash
cp image-source new-image
cp snapshot new-snapshot
qemu-img rebase -b new-image new-snapshot
qemu-img commit new-snapshot
rm new-snapshot
```
The new image will be saved with the other base image, in `/images/`

## React Component
- ### [SandboxManager](https://github.com/remotelabz/remotelabz/blob/master/assets/js/components/Sandbox/SandboxManager.js)
This is the main component that is called by ***react_component*** in the template.<br>
There is only a call to [SandboxList](#sandboxlist) in it but was created for future usage / improvements.<br>
It send a list of **Device** and the **User** data to [SandboxList](#sandboxlist).

- ### [SandboxList](https://github.com/remotelabz/remotelabz/blob/master/assets/js/components/Sandbox/SandboxList.js)
This component process the devices data (given in **json** format by the Controller ealier).
For each **Device** it create a [SandboxListItem](#sandboxlistitem) and sends **Device** and **User** data to it.

- ### [SandboxListItem](https://github.com/remotelabz/remotelabz/blob/master/assets/js/components/Sandbox/SandboxListItem.js)
This is where the main process is done. It manage the 'state' of each device template.<br>
When the component is called, it is going to search if the **Device** as already a Sandbox Lab created for it and the **User**.<br>
If a Sandbox exist, it will show a button to redirect the **User** to the **Device** Sandbox Lab, otherwise It will show the 'Modify' button that will create the Sandbox instance.

- ### [InstanceExport](https://github.com/remotelabz/remotelabz/blob/export-vm/assets/js/components/Instances/InstanceExport.js)
It handle the export form.

## New Endpoints
- ### Web
```
GET /admin/sandbox			- HomePage of Sandbox
GET /admin/sandbox/{labId}	- Sandbox Lab page
```
- ### API
```
GET /api/instances/export/by-uuid/{uuid}?name=		- Export a sandbox device instance
```
