# SMART-MUSEUM-MANAGEMENT-SYSTEM
This is a student project of course "Programming for IoT applications" in Politecnico di Torino. The proposed IoT platform aims at providing services for a smart crowd management in museum.

Links:
* Promote video:
* Demo video: 
* Slides:

# Environment requirement
* System:           Ubuntu 20.04
* Python library:   opencv-python, CherryPy, pickle-mixin, paho-mqtt, requests
* Docker containers: 
```bash
# Pull docker image from docker hub with:
$ docker pull rexyyj/smms:0.1.0
# Create container with:
$ docker run -it --rm rexyyj/smms:0.1.0
# Open and updete the project with:
$ cd SMART-MUSEUM-MANAGEMENT-SYSTEM/ && git pull
```

# Run Demo
The setting of the demo is shown in the figure. Assume we have a small museum with only two zones and three doors. Each zone has a light connector. The main entrance is integrated with laser, motor and camera connector.  The  door and the exit will integrate with laser and motor connector. However, the motor connector on exit will work in “exit” mode, which only allow visitors to leave the museum.
![demo setting](https://github.com/Rexyyj/SMART-MUSEUM-MANAGEMENT-SYSTEM/tree/master/figures/demo.png)
## Step 1: Run home catalog
```bash
# Create a docker container with ip address 172.17.0.2
$ cd homeCat
$ python3 homeCat.py
# Enter the configureation(For test demo, use ip: 172.17.0.2 and port: 8090)
```

## Step 3: Run devices
```bash
# Create a docker container and enter the project
$ cd connectors
$ python3 homeCat.py
# Enter the configureation(For test demo, use ip: 172.17.0.2 and port: 8090)
```