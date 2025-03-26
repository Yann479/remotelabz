remotelabz-docs
===============
[![Build Status](https://jenkins.remotelabz.com/job/remotelabz-docs/job/master/badge/icon)](https://jenkins.remotelabz.com/blue/organizations/jenkins/remotelabz-docs/activity?branch=master)

Documentation of [RemoteLabz](https://gitlab.remotelabz.com/crestic/remotelabz).

# How to use

remotelabz-docs require Python 3, MkDocs and Material for MkDocs.

On Ubuntu 20.04 LTS
```bash
sudo apt-get install python3-pip
pip3 install mkdocs mkdocs-material
```

```bash
git clone https://github.com/remotelabz/remotelabz-docs.git
cd remotelabz-docs
mkdocs build
```

To deploy in local your docs to test it
```bash
mkdocs serve
```
or, if you want to change the listening IP and port
```bash
mkdocs serve -a A.B.C.D:8000
```
