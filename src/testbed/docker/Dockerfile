FROM debian:bullseye

WORKDIR /root

# copy script to setup the testbed experiment container environment
COPY ./scripts/setup.sh setup.sh

# copy script to control the testbed experiment processes
COPY ./scripts/control.sh control.sh

# copy configuration file to serial reader
COPY ./config/config.ini testbed-tsch/testbed-tsch-serial-reader

# copy configuration file to rpc client
COPY ./config/config.ini testbed-tsch/testbed-tsch-rpc-client

# setup the testbed experiment container environment
RUN chmod +x setup.sh && ./setup.sh
