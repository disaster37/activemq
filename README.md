# Table of Contents
- [Introduction](#introduction)
    - [Version](#version)
    - [Changelog](Changelog.md)
- [Hardware Requirements](#hardware-requirements)
    - [CPU](#cpu)
    - [Memory](#memory)
    - [Storage](#storage)
- [Contributing](#contributing)
- [Issues](#issues)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
  - [ACCESS](#access)
  - [QUEUE](#queue)
  - [TOPIC](#topic)
  - [Data Store](#data-store)
  - [BROKER](#broker)
  - [Disk usage](#disk-usage)
  - [JMX](#JMX)
  - [Avaible Configuration Parameters](#avaible-configuration-parameters)
  - [Advance configuration](#advance-configuration)
- [References](#references)

# Introduction

Dockerfile to build a ActiveMQ container image.

## Version

Current Version: **5.15.2**

# Hardware Requirements

## CPU

- No stats avaible to say the number of core in function of messages

## Memory

- 512MB is too little memory, i think is to use ActiveMQ on test environment
- **1GB** is the **standard** memory size

You can set the memory that you need :

```bash
docker run --name='activemq' -it --rm \
	-e 'ACTIVEMQ_CONFIG_MINMEMORY=512' \
	-e 'ACTIVEMQ_CONFIG_MAXMEMORY=2048'\
        -P
	webcenter/activemq:latest
```
This sample lauch ActiveMQ in docker with 512 MB of memory, and then ACtiveMQ can take 2048 MB of max memory

## Storage

The necessary hard drive space depends if you use persistant message or not and the type of appender. Normaly, no need space for ActiveMQ because the most data are contains directly on memory.
I think it depends on how you use ActiveMQ ;)

# Contributing

If you find this image useful here's how you can help:

- Send a Pull Request with your awesome new features and bug fixes
- Help new users with [Issues](https://github.com/disaster37/activemq/issues) they may encounter
- Send me a tip via [Bitcoin](https://www.coinbase.com/disaster37) or using [Gratipay](https://gratipay.com/disaster37/)

# Issues


Fedora and RHEL/CentOS users should try disabling selinux with `setenforce 0` and check if resolves the issue. If it does than there is not much that I can help you with. You can either stick with selinux disabled (not recommended by redhat) or switch to using ubuntu.

If using the latest docker version and/or disabling selinux does not fix the issue then please file a issue request on the [issues](https://github.com/disaster/activemq/issues) page.

In your issue report please make sure you provide the following information:

- The host distribution and release version.
- Output of the `docker version` command
- Output of the `docker info` command
- The `docker run` command you used to run the image (mask out the sensitive bits).

# Installation

Pull the image from the docker index. This is the recommended method of installation as it is easier to update image. These builds are performed by the **Docker Trusted Build** service.

```bash
docker pull webcenter/activemq:5.15.2
```

You can also pull the `latest` tag which is built from the repository *HEAD*

```bash
docker pull webcenter/activemq:latest
```

Alternately you can build the image locally.

```bash
git clone https://github.com/disaster37/activemq.git
cd activemq
docker build --tag="$USER/activemq" .
```

# Quick Start

You can launch the image using the docker command line :

- **For test purpose :**

```bash
docker run --name='activemq' -it --rm -P \
webcenter/activemq:latest
```
The account admin is "admin" and password is "admin". All settings is the default ActiveMQ's settings.

- **For production purpose :**

```bash
docker run --name='activemq' -d \
-e 'ACTIVEMQ_CONFIG_NAME=amqp-srv1' \
-e 'ACTIVEMQ_CONFIG_DEFAULTACCOUNT=false' \
-e 'ACTIVEMQ_ADMIN_LOGIN=admin' -e 'ACTIVEMQ_ADMIN_PASSWORD=your_password' \
-e 'ACTIVEMQ_USERS_myproducer=producerpassword' -e 'ACTIVEMQ_GROUPS_writes=myproducer' \
-e 'ACTIVEMQ_USERS_myconsumer=consumerpassword' -e 'ACTIVEMQ_GROUPS_reads=myconsumer' \
-e 'ACTIVEMQ_JMX_user1_role=readwrite' -e 'ACTIVEMQ_JMX_user1_password=jmx_password' \
-e 'ACTIVEMQ_JMX_user2_role=read' -e 'ACTIVEMQ_JMX_user2_password=jmx2_password'
-e 'ACTIVEMQ_CONFIG_TOPICS_topic1=mytopic1' -e 'ACTIVEMQ_CONFIG_TOPICS_topic2=mytopic2'  \
-e 'ACTIVEMQ_CONFIG_QUEUES_queue1=myqueue1' -e 'ACTIVEMQ_CONFIG_QUEUES_queue2=myqueue2'  \
-e 'ACTIVEMQ_CONFIG_MINMEMORY=1024' -e  'ACTIVEMQ_CONFIG_MAXMEMORY=4096' \
-e 'ACTIVEMQ_CONFIG_SCHEDULERENABLED=true' \
-v /data/activemq:/data \
-v /var/log/activemq:/var/log/activemq \
-p 8161:8161 \
-p 61616:61616 \
-p 61613:61613 \
webcenter/activemq:5.14.3
```


Or you can use [docker-compose](https://docs.docker.com/compose/). Assuming you have docker-compose installed,

```bash
wget https://raw.githubusercontent.com/disaster37/activemq/master/docker-compose.yml
docker-compose up
```

# Configuration

## ACCESS

### Regular users
You can use the following variables to create regular users:
- `ACTIVEMQ_ACTIVEMQ_USERS_X`: Where X is the username and the value is the password.
- `ACTIVEMQ_GROUPS_Y`: Where Y is the group name and the value is the list of user, separated by a comma

You can use the following groups to put right on topic or queue:
- `writes`: can read and write on all topics and queues
- `reads`: can read on all topics and queues
- `owners`: can read, write and own all topics and queues

### Admin user
Or to create administrator, you can use:
- `ACTIVEMQ_ADMIN_LOGIN`: the admin login
- `ACTIVEMQ_ADMIN_PASSWORD`: the admin password

### Disable default account
You can use the following to disable default account:
- `ACTIVEMQ_CONFIG_DEFAULTACCOUNT`: false to disable default account. 

## QUEUE
You can create static queue with the following variable:
- `ACTIVEMQ_CONFIG_QUEUES_X`: Where X is the logical name without special char and the value is the real queue name.

## TOPIC
You can create static topic with the following variable:
- `ACTIVEMQ_CONFIG_TOPICS_X`: Where X is the logical name without special char and the value is the real topic name.

## Data Store
For moment, you can't change the data store. It's kahadb.
The data is store on `/data`.

## BROKER
todo

## Disk usage
You can use the following variables to limit the disk usage:
- `ACTIVEMQ_CONFIG_STOREUSAGE`: the store usage limit. Default is `100 gb`
- `ACTIVEMQ_CONFIG_TEMPUSAGE`: the temp usage limit. Default is `50 gb`

## JMX
You can control JMX access with the following variables:
- `ACTIVEMQ_JMX_X_ROLE`: Where X is the username and the value is the role (read or readwrite)
- `ACTIVEMQ_JMX_X_PASSWORD`: Where X is the username and the value is the password

## Avaible Configuration Parameters

*Please refer the docker run command options for the `--env-file` flag where you can specify all required environment variables in a single file. This will save you from writing a potentially long docker run command. Alternately you can use docker-compose.*

### Confd

The ActiveMQ setting is managed by Confd. So you can custom it:
- **CONFD_BACKEND**: The Confd backend that you should use. Default is `env`.
- **CONFD_NODES**: The array of Confd URL to contact the backend. No default value.
- **CONFD_PREFIX_KEY**: The Confd prefix key. Default is `/activemq`

### ActiveMQ parameters

Below is the complete list of available options that can be used to customize your activemq installation.

- **ACTIVEMQ_CONFIG_NAME**: The hostname of ActiveMQ server. Default to `localhost`
- **ACTIVEMQ_LOGGER_LOGLEVEL**: The log level. Default to `INFO`
- **ACTIVEMQ_CONFIG_PENDINGMESSAGELIMIT**: It is used to prevent slow topic consumers to block producers and affect other consumers by limiting the number of messages that are retained. Default to `1000`
- **ACTIVEMQ_CONFIG_STORAGEUSAGE**: The maximum amount of space storage the broker will use before disabling caching and/or slowing down producers. Default to `100 gb`
- **ACTIVEMQ_CONFIG_TEMPUSAGE**: The maximum amount of space temp the broker will use before disabling caching and/or slowing down producers. Default to `50 gb`
- **ACTIVEMQ_CONFIG_MAXCONNECTION**: It's DOS protection. It limit concurrent connections. Default to `1000`
- **ACTIVEMQ_CONFIG_FRAMESIZE**: It's DOS protection. It limit the frame size. Default to `104857600` (100MB)
- **ACTIVEMQ_CONFIG_SCHEDULERENABLED**: Permit to enabled scheduler in ActiveMQ. Default to `true`
- **ACTIVEMQ_CONFIG_AUTHENABLED**: Permit to enabled the authentification in queue and topic (no anonymous access). Default to `false`
- **ACTIVEMQ_CONFIG_MINMEMORY**: The init memory in MB that ActiveMQ take when start (it's like XMS). Default to `128` (128 MB)
- **ACTIVEMQ_CONFIG_MAXMEMORY**: The max memory in MB that ActiveMQ can take (it's like XMX). Default to `1024` (1024 MB)

- **ACTIVEMQ_DEFAULTACCOUNT**: It's permit to remove all default login on ActiveMQ (Webconsole, broker and JMX). Default to `true`
- **ACTIVEMQ_ADMIN_LOGIN**: The login for admin account (broker and web console). Default to `admin`
- **ACTIVEMQ_ADMIN_PASSWORD**: The password for admin account. Default to `admin`
- **ACTIVEMQ_USERS_X**: Where X is the username and password is the value.
- **ACTIVEMQ_GROUPS_X**: Where X is the group and list user separated by a comma is the value. 
- **ACTIVEMQ_JMX_X_ROLE**: Where X is the username and role is the value.
- **ACTIVEMQ_JMX_X_PASSWORD**: Where X is the username and password is the value.

- **ACTIVEMQ_CONFIG_TOPICS_X**: Where X is the logical topics name (wihtout special char) and real topic name is the value.
- **ACTIVEMQ_CONFIG_QUEUES_X**: Where X is the logical queue name (wihtout special char) and real queue name is the value.


## Advance configuration

For advance configuration, the best way is to read ActiveMQ documentation and created your own setting file like activemq.xml.
Next, you can mount it when you run this image or you can create your own image (base on this image) and include your specifics config file.

The home of ActiveMQ is in /opt/activemq, so if you want to override all the setting, you can launch docker with ` -v /your_path/conf:/opt/activemq/conf`.
If you overload the config, don't forget to disable confd or change the template instead to change activemq config `/opt/confd/etc/templates`.