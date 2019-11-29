# Docker

Docker is a  OS-level virtualization software used to deliver software in packages called containers.

## Install

- From Debian: Follow instruction on <a href="https://docs.docker.com/install/linux/docker-ce/debian/">docker docs</a>
- From Windows: You need to install <a href="https://www.docker.com/products/docker-desktop">Docker Desktop</a> which will create a kind of Linux VM in order to use Docker properly.

## Community

You can find a lot of base image in <a href="https://hub.docker.com/search?type=image">docker hub</a>

## Basic commands

### Handling images

|Command|Description|
|-------|-----------|
|`docker image ls`|List all base images|
|`docker image rm [IMAGE NAMES]`|Remove images|

### Handling containers

|Command|Description|
|-------|-----------|
|`docker ps`|List running containers|
|`docker container ls -a`|List all containers|
|`docker run [OPTIONS] --name [NAME FOR YOUR CONTAINER] [IMAGE NAME] [POTENTIAL COMMAND]`|Create and launch a new container using an image|
|`docker stop [CONTAINER ID OR NAME]`|Stop a running container (will not be deleted)|
|`docker container start [CONTAINER ID OR NAME]`|Start a container that was already launched before|
|`docker container rm [CONTAINER IDS OR NAMES]`|Remove containers (must be stopped before or add `-f` to force remove)|
|`docker exec -t -i [CONTAINER ID OR NAME] [COMMAND]`|Execute command in container|

### Maintenance
|Command|Description|
|-------|-----------|
|`docker export [CONTAINER NAME] \| gzip > [CONTAINER NAME].gz`|Export a container|
|`zcat [CONTAINER NAME].gz \| docker import - [CONTAINER NAME]`|Import a container|

## Creating an image and container (full explanation)

### Basic build example

In an empty folder, create a `DockerFile` file with this content:
```
FROM ubuntu

USER root

RUN apt-get update
RUN apt-get -y upgrade
```

Launch this command from the folder containing the `DockerFile`:
`docker built -t [MY NEW IMAGE NAME IN LOWERCASE] .`
You now have an updated ubuntu image!

Note: You can build in a not empty folder but you should ignore files you don't want by specifying them in a `.dockerignore` file.

### More information about DockerFile

|Command|Description|
|-------|-----------|
|`FROM [base image name]`|Image to use as base for our new image|
|`MAINTENER [name]`|Specify the maintainer name|
|`RUN [command]`|Execute specific command to build the image|
|`COPY [FROM (local folder)] [TO (in docker image)]`|Add file in the image|
|`WORKDIR [NEW PATH]`|Change work directory (all next command will be executed there)|
|`EXPOSE [PORT NUMBER]`|Expose a port to the outside of the container|
|`VOLUME [FOLDER IN THE CONTAINER]`|Expose a folder to the outside of the container|
|`CMD [command]`|Commands to execute when starting the container|

More information can be found here: https://docs.docker.com/engine/reference/builder/

### Create and launch a new container

`docker run [SOME OPTIONS] --name [NAME TO GIVE TO YOUR CONTAINER] [IMAGE TO USE] [POTENTIAL CMD]`

|Option|Description|Link with Dockerfile|
|------|-----------|--------------------|
|`-v [local folder]:[container folder]`|Share container folder with a local folder|`VOLUME`|
|`-p [local port]:[container port]`|Access the container port|`EXPOSE`|
|`-d`|Launch the container in a deamon (background)||
|`-it`|Launch the container in interactive mode in your command prompt)||
|`--rm`|Remove the container once the container exit||
