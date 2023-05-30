FROM debian:bullseye

WORKDIR /root

# copy script to setup the testbed experiment container environment
COPY ./scripts/setup.sh setup.sh
RUN chmod +x setup.sh 

# copy script to control the testbed experiment processes
COPY ./scripts/control control
RUN chmod +x control/*

# copy configuration file
COPY ./config/config.ini config.ini

# setup the testbed experiment container environment
RUN ./setup.sh

# put the ARM compiler path in the PATH
ENV PATH "/root/arm-compiler/gcc-arm-none-eabi-9-2020-q2-update/bin:$PATH"

# Change to Control Script module directory
WORKDIR /root/testbed-tsch/control
