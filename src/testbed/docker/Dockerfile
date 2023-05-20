FROM debian:bullseye

WORKDIR /root

# copy script to setup the testbed experiment container environment
COPY ./scripts/setup.sh setup.sh
RUN chmod +x setup.sh 

# copy script to control the testbed experiment processes
COPY ./scripts/control.sh control.sh
RUN chmod +x control.sh 

# copy configuration file to serial reader
COPY ./config/config.ini config.ini

# copy configuration file to rpc client
COPY ./config/config.ini config.ini

# setup the testbed experiment container environment
RUN ./setup.sh
