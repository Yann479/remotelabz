#Contribute to RemoteLabz

The RemoteLabz project source code is hosted on GitHub at https://github.com/remotelabz/ and always welcome new contributors !

There is five different repositories for this project:

* Remotelabz : RemoteLabz front interface.
* Remotelabz-worker: RemoteLabz VM management side.
* Remotelabz-docs : RemoteLabz document component (this guide's repository)
* Network-bundle : A module used by RemoteLabz to handle all IP and network aspects.
* Remotelabz-message-bundle: Another module that handles shared messages between RemoteLabz workers and the front. 

If you wish to contribute, here the steps.
## Commit code on the repositories
###Sign your Code

If you need to commit code, you have to sign it first. 

For Mac and Windows there is a complete guide at https://github.com/microsoft/vscode/wiki/Commit-Signing

Here we will focus on ubuntu 

First install git and gpg (if not already installed)

```bash
apt-get install git
apt-get install gpg
```

To push code on RemoteLabz repositories, you need to sign your commits with a key linked up to your account.
First create a key with the command
```bash
gpg --full-generate-key
```
Answer all the questions
At the end of the process a key with a key ID is generated
![Screenshot](/images/Developers/git_images/gpg_key_generated.png)


Retrieve your key ID by using the command
```bash
gpg --list-secret-keys --keyid-format=long
```
![Screenshot](/images/Developers/git_images/gpg_key_list.png)
Then export the key using the retrieved ID.

```bash
gpg --armor --export your_key_ID
```
then go to your github account and add the key in your account -> settings -> ssh and gpg keys -> add key 


For more informations, you can follow <a href="https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account"> this guide</a>

Once you've added the key, you will need to order git to sign the commits.But first, Git needs to know that your key exists.
```bash
git config --global user.signingkey <Your Key ID>
```
Then it must be told to use it when signing the commits

```bash
git config --global commit.gpgsign true
```
###Integrating Git to Visual Studio Code
If you wish to use Git alongside Visual Studio, you need to do the following.

On VSCode, go to plugins and install the Git Extension Pack.
![Screenshot](/images/Developers/git_images/vscode_git_add.png)

Then, into settings, go to Extension->Git and tick the box `Git enable commit signing`
![Screenshot](/images/Developers/git_images/vscode_git_code_signing.png)

##Documentation

You can find a copy of this guide on the following GitHub Page:

https://github.com/remotelabz/remotelabz-docs

You can clone it from there using 

```
git clone https://github.com/remotelabz/remotelabz-docs.git
```

###Self hosting

You can self-host this guide for editing and testing purposes.

You will need MKdocs to properly host and display these files.Mkdocs converts templates files (.md) into HTML pages.


remotelabz-docs require Python 3, MkDocs and Material for MkDocs.

If you are On Ubuntu 20.04 LTS

```
sudo apt-get install python3-pip
pip3 install mkdocs mkdocs-material

```

In order to display the documentation on a local server (for instance if you need to test before commiting anything), enter these commands.
Here an example for the URL address http://192.168.11.131:8040 :

To build documentation prior to push :
``` bash
mkdocs build
```

``` bash 
mkdocs serve --dev-addr 192.168.11.131:8040
```


