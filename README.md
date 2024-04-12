# SDLE Second Assignment

SDLE Second Assignment of group T1G17.

This project consists in a social network, which the users are able to post as well as follow and unfollow other users.
But this social network uses peer-to-peer networking to transmit information inside it.

## Python Dependencies
All python librarires needed:
```s
Flask==2.2.2
Flask_Cors==3.0.10
kademlia==2.2.2
python_bcrypt==0.3.2
pyzmq==24.0.1
```

## Application Usage
```
main.py [-h] -i IP -kp KADEMLIA_PORT -mp MESSAGE_PORT [-ap API_PORT -n NODE NODE]

  -h, --help            show this help message and exit
  -i IP, --ip IP        ip address of current node
  -kp KADEMLIA_PORT, --kademlia_port KADEMLIA_PORT
                        kademlia port number of current node
  -mp MESSAGE_PORT, --message_port MESSAGE_PORT
                        server port number of current node
  -ap API_PORT, --api_port API_PORT
                        api port number of current node
  -n NODE_IP NODE_PORT, --node NODE NODE
                        ip and port of bootstrap node

```

(The following commands are supposed to be run from the project root folder, not inside the src)

## Terminal Version

In the terminal version, we mustn't fill the -ap flag.

### Example of usage:
Running the bootsrap node:
```
python3 -m src.main -i 127.0.0.1 -kp 8001 -mp 9001
```
A new node connecting using the bootstrap node:
```
python3 -m src.main -i 127.0.0.2 -kp 8002 -mp 9002 -n 127.0.0.1 8001
```

## Frontend Version

In the frontend version, we must fill the -ap flag, and also run the React application with the environment variable ``REACT_APP_API_PORT`` set to the same value of the api_port of the python program. To make the usage simple, we have 4 scripts that create four different nodes for testing purposes.
It's also important to run ``npm install`` inside the src/frontend folder before the following commands.

### Example of usage:

It's simple to use it, run the following commands, one in a different terminal. It's important to run the ``bootstrap.sh`` first of all.

Bootstrap:

```
./bootstrap.sh
```
Nodes:
```
./node1.sh
```
```
./node2.sh``
```
```
./node3.sh``
```
```
./node4.sh
```

After using the network, and killing all the terminal instances, it's important to run the ``kill_all_react_instances.sh`` script as well, to kill the React instances running in the background.

## Group members:

1. Amanda Oliveira (up201800698@fe.up.pt).
2. Filipe Pinto (up201907747@fe.up.pt).
3. Pedro Carvalho (up201900513@fe.up.pt).
4. Victor Nunes (up201907226@fe.up.pt).
