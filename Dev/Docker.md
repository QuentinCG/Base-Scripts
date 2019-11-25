# Docker

Docker is a  OS-level virtualization software used to deliver software in packages called containers.

## Install

- From Debian: Follow instruction on <a href="https://docs.docker.com/install/linux/docker-ce/debian/">docker docs</a>
- From Windows: You need to install <a href="https://www.docker.com/products/docker-desktop">Docker Desktop</a> which will create a kind of Linux VM in order to use Docker properly.

## Community

You can find a lot of base image in <a href="https://hub.docker.com/search?type=image">docker hub</a>

## Basic commands

Handling images:
- List all base images: `docker image ls`
- Remove images: `docker image rm [IMAGE NAMES]`

Handling containers:
- List running containers: `docker ps`
- List all containers: `docker container ls -a`
- Launch a new container using an image: `docker run --name [ANY NAME YOU WANT FOR YOUR CONTAINER] [IMAGE NAME]` (a lot of options are possible like exposing port: `-p [PORT IN HOST SIDE]:[PORT IN IMAGE SIDE]`)
- Stop a running container (will not be deleted): `docker stop [CONTAINER ID OR NAME]`
- Start a container that was already launched before: `docker container start [CONTAINER ID OR NAME]`
- Remove containers (must be stopped before): `docker container rm [CONTAINER IDS OR NAMES]`

## Creating an image

# Basic example

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
