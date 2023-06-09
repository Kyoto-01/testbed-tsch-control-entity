#!/usr/bin/env bash

# Set Testbed TSCH modules repository link

FIRMWARE_REPOSITORY="https://github.com/Kyoto-01/testbed-tsch-firmware.git"

SERIAL_READER_REPOSITORY="https://github.com/Kyoto-01/testbed-tsch-serial-reader.git"

RPC_CLIENT_REPOSITORY="https://github.com/Kyoto-01/testbed-tsch-rpc-client.git"


# Install dependencies

apt update && apt upgrade -y

apt install -y \
    build-essential \
    git \
    git-lfs \
    curl \
    wget \
    srecord \
    rlwrap

apt install -y \
    python3-pip \
    python3-serial

python3 -m pip install virtualenv

## Install and setup ARM compiler dependency

mkdir ~/arm-compiler

cd ~/arm-compiler

wget https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu-rm/9-2020q2/gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2

tar -xjf gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2

echo "if [ -d \"\$HOME/arm-compiler/gcc-arm-none-eabi-9-2020-q2-update/bin\" ] ; then \
PATH=\"\$HOME/arm-compiler/gcc-arm-none-eabi-9-2020-q2-update/bin:\$PATH\"; fi" >> ~/.profile

echo 'ATTRS{idVendor}=="0451", ATTRS{idProduct}=="16c8", ENV{ID_MM_DEVICE_IGNORE}="1"' >> /lib/udev/rules.d/77-mm-usb-device-blacklist.rules

# Create testbed structure

mkdir ~/testbed-tsch

cd ~/testbed-tsch

mv ~/control . 

git clone ${FIRMWARE_REPOSITORY}

git clone ${SERIAL_READER_REPOSITORY}

git clone ${RPC_CLIENT_REPOSITORY}

# Create modules configuration files

cp ~/config.ini control

cp ~/config.ini testbed-tsch-serial-reader

cp ~/config.ini testbed-tsch-rpc-client

# Create and setup Python 3 virtual environments

mkdir ~/venvs

cd ~/venvs

python3 -m virtualenv testbed-tsch-control-script
source testbed-tsch-control-script/bin/activate
python3 -m  pip install -r ~/testbed-tsch/control/requirements.txt
deactivate

python3 -m virtualenv testbed-tsch-firmware
source testbed-tsch-firmware/bin/activate
python3 -m  pip install -r ~/testbed-tsch/testbed-tsch-firmware/tools/testbed-build/requirements.txt
deactivate

python3 -m virtualenv testbed-tsch-serial-reader
source testbed-tsch-serial-reader/bin/activate
python3 -m  pip install -r ~/testbed-tsch/testbed-tsch-serial-reader/requirements.txt
deactivate

python3 -m virtualenv testbed-tsch-rpc-client
source testbed-tsch-rpc-client/bin/activate
python3 -m  pip install -r ~/testbed-tsch/testbed-tsch-rpc-client/requirements.txt
deactivate
