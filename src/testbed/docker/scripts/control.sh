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

## module parameters

build_tool_parameters=""

serial_reader_parameters=""

rpc_client_parameters=""
 
param=""
for a in $@; do
    case ${param} in
    "--action") 
        action=${a} 
    ;;
    "--firmtxpwr") 
        firmtxpwr=${a}
        build_tool_parameters="${build_tool_parameters} -p ${a}"
    ;;
    "--firmtxintv")
        firmtxintv=${a}
        build_tool_parameters="${build_tool_parameters} -i ${a}"
    ;;
    "--firmhslen")
        firmhslen=${a} 
        build_tool_parameters="${build_tool_parameters} -l ${a}"
    ;;
    "--firmhopseq") 
        firmhopseq=${a} 
        build_tool_parameters="${build_tool_parameters} -h ${a}"
    ;;
    "--usbports") 
        usbports=${a}
        build_tool_parameters="${build_tool_parameters} -u ${a}"
        serial_reader_parameters="${serial_reader_parameters} -p ${a}"
    ;;
    "--testbed") 
        testbed=${a}
        serial_reader_parameters="${serial_reader_parameters} -t ${a}"
        rpc_client_parameters="${rpc_client_parameters} -t ${a}"
    ;;
    "--analyzeintv") 
        analyzeintv=${a}
        rpc_client_parameters="${rpc_client_parameters} -i ${a}"
    ;;
    esac
    param=${a}
done

# create file to store testbed processes PIDs

touch ~/pids

if [ ${action} == "start" ];
then

    # Writing client/server firmwares in testbed motes

    source ~/venvs/testbed-tsch-firmware/bin/activate
    cd ~/testbed-tsch/testbed-tsch-firmware/tools/testbed-build
    eval "./testbed-build.sh -f all ${build_tool_parameters}"

    # start serial reader

    source ~/venvs/testbed-tsch-serial-reader/bin/activate
    cd ~/testbed-tsch/testbed-tsch-serial-reader/src
    eval "./main.py ${serial_reader_parameters} &"
    echo $! >> ~/pids

    # start RPC client

    source ~/venvs/testbed-tsch-rpc-client/bin/activate
    cd ~/testbed-tsch/testbed-tsch-rpc-client/src
    eval "./main.py -r analyze -g all ${rpc_client_parameters} &"
    echo $! >> ~/pids

    cd ~

elif [ ${action} == "stop" ];
then

    # kill testbed pocesses

    for pid in $(cat ~/pids);
    do
        kill -9 ${pid}
    done

    # Writing stopped firmware in testbed motes

    source ~/venvs/testbed-tsch-firmware/bin/activate
    cd ~/testbed-tsch/testbed-tsch-firmware/tools/testbed-build
    eval "./testbed-build.sh -f stopped ${build_tool_parameters}"

    # clear testbed processes PIDs file

    rm -f ~/pids

    cd ~
fi
