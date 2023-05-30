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

if [ "${action}" == "start" ];
then

    # Record testbed start action in database

    source ~/venvs/testbed-tsch-control-script/bin/activate
    cd ~/testbed-tsch/control
    ./control_db.py --action start --testbed ${testbed}

    # create file to store testbed processes PIDs

    touch ~/pids

    # Writing client/server firmwares in testbed motes

    source ~/venvs/testbed-tsch-firmware/bin/activate
    cd ~/testbed-tsch/testbed-tsch-firmware/tools/testbed-build
    eval "./testbed-build.sh -f all ${build_tool_parameters}"

    # start serial reader

    source ~/venvs/testbed-tsch-serial-reader/bin/activate
    cd ~/testbed-tsch/testbed-tsch-serial-reader/src
    eval "./main.py ${serial_reader_parameters} &"

    SERIAL_READER_PID=$!

    echo "${SERIAL_READER_PID}" >> ~/pids

    # start RPC client

    source ~/venvs/testbed-tsch-rpc-client/bin/activate
    cd ~/testbed-tsch/testbed-tsch-rpc-client/src
    eval "./main.py -r analyze -g all ${rpc_client_parameters} &"

    RPC_CLIENT_PID=$!

    echo "${RPC_CLIENT_PID}" >> ~/pids

    # start print logs

    uptime=0

    while [ -f "${HOME}/pids" ];
    do
        echo "running: ${testbed} (${uptime} seconds)"
        echo "(Serial Reader: ${SERIAL_READER_PID}; RPC Client: ${RPC_CLIENT_PID})"

        uptime=$(( ${uptime} + 5 ))
        
        sleep 5
    done

elif [ "${action}" == "stop" ];
then

    # Record testbed stop action in database

    source ~/venvs/testbed-tsch-control-script/bin/activate
    cd ~/testbed-tsch/control
    ./control_db.py --action stop --testbed ${testbed}

    # kill testbed pocesses

    if [ -f "${HOME}/pids" ];
    then
        for pid in $(cat ~/pids);
        do
            kill -9 ${pid}
        done
    fi

    # Writing stopped firmware in testbed motes

    source ~/venvs/testbed-tsch-firmware/bin/activate
    cd ~/testbed-tsch/testbed-tsch-firmware/tools/testbed-build
    eval "./testbed-build.sh -f stopped ${build_tool_parameters}"

    if [ -f "${HOME}/pids" ];
    then
        rm -f ~/pids
    fi

fi
