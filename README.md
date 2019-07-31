# QTCPServer


## SERVER
Help: `python server.py --help`

```
usage: server.py [-h] [--HOST HOST] [--PORT PORT] [--socket]

Run a TCP Server waiting for client to connect and send data

optional arguments:
  -h, --help   show this help message and exit
  --HOST HOST  host IP
  --PORT PORT  commmunication port
  --socket     use socket instead of QTCPSocket (deprecated)
```

Example:

`python server.py --HOST localhost --PORT 1235`

`python server.py --HOST 10.68.74.44 --PORT 1235 --socket`


# DOCKER

build docker:

`sudo docker build . -t qtcpserver`

run docker:
`sudo docker run -p 1346:1346 --rm --runtime=nvidia -ti qtcpserver`


tag image ID
`sudo docker tag qtcpserver:latest silviogiancola/qtcpserver:latest`

push modification to docker.io:

`sudo docker push silviogiancola/qtcpserver:latest`
