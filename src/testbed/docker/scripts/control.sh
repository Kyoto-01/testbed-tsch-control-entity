#!/usr/bin/env bash

# Processing parameters

## action to execute in testbed
action=""

## testbed motes tx power
firmtxpwr=""

## testbed motes tx interval
firmtxintv=""

## testbed motes channel hop sequence length
firmhslen=""

## testbed motes channel hop sequence in format <ch0>,<ch1>,...,<chn>
firmhopseq=""

## testbed allocated usb ports
usbports=""

## testbed name
testbed=""

## testbed analyze rpc client request interval
analyzeintv=""

param=""
for a in $@; do
    case ${param} in
    "--action") action=${a} ;;
    "--firmtxpwr") firmtxpwr=${a} ;;
    "--firmtxintv") firmtxintv=${a} ;;
    "--firmhslen") firmhslen=${a} ;;
    "--firmhopseq") firmhopseq=${a} ;;
    "--usbports") usbports=${a} ;;
    "--testbed") testbed=${a} ;;
    "--analyzeintv") analyzeintv=${a} ;;
    esac
    param=${a}
done

if [ ${action} == "start" ];
then
    # Writing client/server firmwares in testbed motes

    bash
    source ~/venvs/testbed-tsch-firmware/bin/activate
    cd ~/testbed-tsch/testbed-tsch-firmware/tools/testbed-build
    ./testbed-build.sh \
        -f all \
        -u ${usbports} \
        -p ${firmtxpwr} \
        -i ${firmtxintv} \
        -l ${firmhslen} \
        -h ${firmhopseq}

    # start serial reader

    bash
    source ~/venvs/testbed-tsch-serial-reader/bin/activate
    cd ~/testbed-tsch/testbed-tsch-serial-reader/
    ./main \
        -t ${testbed} \
        -p ${usbports}

    # start RPC client

    bash
    source ~/venvs/testbed-tsch-rpc-client/bin/activate
    cd ~/testbed-tsch/testbed-tsch-rpc-client/
    ./main \
        -i ${analyzeintv} \
        -r analyze \
        -g all \
        -t ${testbed}

    bash
    cd ~

elif [ ${action} == "stop" ];
then
    # Writing stopped firmware in testbed motes

    bash
    source ~/venvs/testbed-tsch-firmware/bin/activate
    cd ~/testbed-tsch/testbed-tsch-firmware/tools/testbed-build
    ./testbed-build.sh \
        -f stopped \
        -u ${usbports} \

    bash
    cd ~
fi
