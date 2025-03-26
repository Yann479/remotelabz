# States Messages

The Front and the Worker exchange messages from bundle remotelabz/remotelabz-message-bundle. The Front send Action message and the Worker answer with Stage message.

When a user starts a lab, a message (json) is sent to the worker and analyzed by ```MessageHandler/InstanceActionMessageHandler.php```. The instance, which is a started lab, is managed by the Instance Manager service in ```Service/Instance/InstanceManager.php```

The action is related instance and from version 2.4.0 :

 - Create (Lab)
 - Delete (Lab and Device)
 - Start (Device)
 - Stop (Device)
 - Export (Device).

The worker answers, respectively, with the state : 

 - Created
 - Deleted
 - Started
 - Stopped
 - Exported.

Another state is added : the state Error.
