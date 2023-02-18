# Deployment of application to cloud server

## Setting up Vagrant and VirtualBox

An installation of Vagrant and VirtualBox is needed to intitialize and start the VM which runs our application and is hosted on DigitalOcean's cloud servers.

For Windows users, follow this guide for both installations: https://www.itu.dk/people/ropf/blog/vagrant_install.html

For Linxus users, the following commands will install Vagrant:

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant
```

And VirtualBox:

```bash
sudo apt install virtualbox virtualbox-ext-pack
```

Vagrant plugins (can be run in Git Bash for Windows users):

```bash
vagrant plugin install vagrant-digitalocean
vagrant plugin install vagrant-scp
vagrant plugin install vagrant-vbguest
vagrant plugin install vagrant-reload
```

## Using Vagrant to start the VM

Standing in the folder 'VagrantMiniTwit' located in the root of this repository, run the following to clean old Vagrant files:

```bash
rm -r .vagrant/
```

Then, run the following to boot up the VM which is hosted on a DigitalOcean cloud server, creating a Docker image of the application and runs it:

```bash
vagrant up
```

After a couple of minutes an URL of the running application should be echo'd in the terminal.

## Destroying the VM

To destroy the VM running the application, run the following command:

```bash
vagrant destroy
```

A prompt to verify the destruction should appear (simply say 'y' and ENTER). Additionally, the following command can be used to check the status of the VM:

```bash
vagrant status
```