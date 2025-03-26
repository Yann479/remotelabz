#Setup local documentation server

##Overview

You can find a copy of remotelabz local documentation on the following GitHub Page:

https://github.com/remotelabz/remotelabz-docs

You can clone it from there using 

```
git clone https://github.com/remotelabz/remotelabz-docs.git
```

You will need MKdocs to properly host and display these files.Mkdocs converts templates files (.md) into HTML pages.

#Mkdocs installation
remotelabz-docs require Python 3, MkDocs and Material for MkDocs.

If you are On Ubuntu 20.04 LTS

```
sudo apt-get install python3-pip
pip3 install mkdocs mkdocs-material

```

##Mkdocs commands

In order to display the documentation on a local server (for instance if you need to test before commiting anything), enter these commands.
Here an example for the URL address http://192.168.11.131:8040 :

To build documentation prior to push :
``` bash
mkdocs build
```

``` bash 
mkdocs serve --dev-addr 192.168.11.131:8040
```
##Code organisation

The file used with all the links are defined in

``` bash
docs/mkdocs.yml
```
The other source files are on the `/docs` Directory

The images files are on the `/site/images` Directory


