FROM ubuntu:latest
RUN apt-get update && apt-get install python3-pip git vim net-tools -y
RUN pip3 install opencv-python CherryPy pickle-mixin paho-mqtt requests
RUN rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/Rexyyj/SMART-MUSEUM-MANAGEMENT-SYSTEM.git
