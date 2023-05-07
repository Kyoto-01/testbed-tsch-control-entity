#!/usr/bin/env bash

VENVS_DIR="${HOME}/venvs"

MODULE_VENV_NAME="testbed-tsch-rpc-client-venv"

MODULE_DIR="${HOME}/testbed-tsch/testbed-tsch-rpc-client"

MODULE_EXEC_DIR="${MODULE_DIR}/src"

MODULE_EXEC_FILE="main.py"

args=$1

source ${PWD}/control/process/start_module.sh
