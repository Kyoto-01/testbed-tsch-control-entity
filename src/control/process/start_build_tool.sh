#!/usr/bin/env bash

VENVS_DIR="${HOME}/venvs"

MODULE_VENV_NAME="testbed-tsch-firmware-venv"

MODULE_DIR="${HOME}/testbed-tsch/testbed-tsch-firmware/tools/testbed-build"

MODULE_EXEC_DIR=${MODULE_DIR}

MODULE_EXEC_FILE="testbed-build.sh"

args=$1

source ${PWD}/control/process/start_module.sh
