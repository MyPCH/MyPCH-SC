# Quick up-and-running

The aim is to establish various [demos](../demos/README.md) of software solutions for the MyPCH project around the Tidepool platform (https://www.tidepool.org) and Semantic Container (https://www.ownyourdata.eu/en/semcon/).

## Prerequisites

- A machine running Ubuntu 18.04 LTS (20.04 LTS is not recommended)
- Install `docker` and `docker-compose`. The process described at https://docs.docker.com/engine/install/ubuntu is fine, i.e.,:

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Add your user to the docker group, so docker commands can be run without `sudo`:

```bash
sudo usermod -aG docker $USER
sudo newgrp docker  # will activate this for your user, without a reboot
```

## Tidepool
From Tidepool we use the development repo to get the platform at a local instans. The uploader repo contains the an extract utility 


### Steps for creating repos
1. Create a new folder, e.g tidepool-development, to hold all the Tidepool repos.
```
mkdir tidepool-development
cd tidepool-development
```

2. Clone Tidepool development, uploader, blip

Recommend to use the same names as Tidepool to avoid changing in code.
```
git clone https://github.com/tidepool-org/development development
git clone https://github.com/tidepool-org/uploader uploader
git clone https://github.com/tidepool-org/blip blip
```

3. Set path  
Avoid `PATH` problems. Use your `~/.bashrc` file.
Remember to be in under tidepool-development repository
```
cd tidepool-development
echo "export PATH=${PWD}/bin:${PATH}" >> ~/.bashrc
exec bash

```

### Steps to get it up running
The process to get Tidepool running with a local Kubernetes cluster is well described https://github.com/tidepool-org/development/tree/k8s-stable
Please remember that you need to check out this branch.

```
git fetch -ap
git checkout -b k8s-stable origin/k8s-stable
```

Different versions were listed in the documentation of Tidepool. This is just copying it here:

```
# Linux
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.1/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

# Linux
curl -fsSL https://get.helm.sh/helm-v3.0.2-linux-amd64.tar.gz | tar -xzv linux-amd64 && sudo mv linux-amd64/helm /usr/local/bin/helm

# Linux
curl -fsSL https://github.com/windmilleng/tilt/releases/download/v0.11.4/tilt.0.11.4.linux.x86_64.tar.gz | tar -xzv tilt && sudo mv tilt /usr/local/bin/tilt
```
You need also to create a directory for MongoDB data.

```
export TIDEPOOL_DOCKER_MONGO_VOLUME="~/MyMongoData" 
```

The process with the `tidepool` helper scripts involves:

`tidepool server-init`

Please remember to add `export KUBECONFIG=${HOME}/.kube/config` to your `.bashrc` file, and do `exec bash` to reload the configuration.
You might need to do `mkdir ~/.kube` first.

## Smoketest web

`tidepool start` will bring everything up, and you can access http://localhost:3000 and then create a user. 

### Create user account
The account verification can be done using:

`tidepool verify-account-email <email>`

### Debug
The tidepool services can behave a bit oddly. In this case, it may be required to delete the images. The `tidepool` utility provides a wrapper for docker to prune/delete the relevant images. The images and containers are stateless.

Check prerequisites:
```
tidepool doctor
```

Stop server
```
tidepool stop (in a new terminal)
tidepool server-prune (if stop not works)
```

Start server:
```
tidepool server-init
tidepool start
```

# Uploader

The uploader service needs to be prepared.

The Tidepool uploader can easy be launched on a Linux platform using the Docker container, thanks to Tim (@TheDukeDK) and Mads (@atombrella) from Denmark. 

If you are running Linux you probably need to be using an Ubuntu distribution or derivative. To get around this for other distrubutions you can try to build a local docker image which is based on Ubuntu 18.04 and use the yarn/npm commands interactively.

The process is described in the documentation https://github.com/tidepool-org/uploader#docker-for-linux

**NOTE:** You need to add udev rules to your host for uploads to actually work. You can find the udev rules [here](resources/linux/51-tidepool-uploader.rules). The file should be placed in `/etc/udev/rules.d/` and the host should be rebooted.


1. Build the image
    `docker-compose build` 
    
2. Run it
    `docker-compose up -d` 


Making a new Windows or MacOS package is feasible with

```bash
docker exec -it uploader bash -c "yarn package-win"  # or package-mac or package-all
```

It should leave the files in the host.

## Smoketest uploader
Test on the client and work with it interactively. 

Even if you kill the Tidepool Uploader GUI the container will continue to run. You can work with the yarn commands like you would locally by using docker exec.

**Examples**

Interactively select the yarn target: `docker exec -it uploader bash -c "yarn run"`

Rebuild: `docker exec -it uploader bash -c "yarn build"`

Start the Dev GUI: `docker exec -it uploader bash -c "yarn dev"`

## Semantic Container
The fork in MyPCH https://github.com/MyPCH/sc-diabetes is based on the original upstream source that can be found at https://github.com/sem-con/sc-diabetes

Clone the sc-diabetes semantic container repo from orginal upstream to get the newest version:

```bash
git clone https://github.com/sem-con/sc-diabetes.git  
```

## SC demonstrations
In the folder dataflows the demonstation of Semantic capabilities can found at these links:
* [Tidepool integration](https://github.com/sem-con/sc-diabetes/blob/master/dataflows/Tidepool_Integration/README.md)
* [Personal Data](https://github.com/sem-con/sc-diabetes/tree/master/dataflows/Personal_Data)
* [Data Donation](https://github.com/sem-con/sc-diabetes/blob/master/dataflows/Data_Donation/README.md)
* [Data Tracing](https://github.com/sem-con/sc-diabetes/blob/master/dataflows/Data_Tracing/README.md)





