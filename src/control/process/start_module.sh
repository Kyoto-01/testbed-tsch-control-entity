# create python3 virtual environments directory
if ! ls ${VENVS_DIR} &> /dev/null;
then
    mkdir ${VENVS_DIR}
fi

# create and setup python3 virtual environment to Testbed TSCH Firmware module
if ! ls ${VENVS_DIR}/${MODULE_VENV_NAME} &> /dev/null;
then
    cd ${VENVS_DIR}
    python3 -m virtualenv ${MODULE_VENV_NAME}
    source ${VENVS_DIR}/${MODULE_VENV_NAME}/bin/activate
    pip3 install -r ${MODULE_DIR}/requirements.txt
    deactivate
fi

# set virtual environment
source ${VENVS_DIR}/${MODULE_VENV_NAME}/bin/activate

cd ${MODULE_EXEC_DIR}

eval "./${MODULE_EXEC_FILE} ${args} &"

PID=$!

function trap_ctrlc() {
    kill -9 ${PID}
    exit 2
}

trap "trap_ctrlc" 2

while ps -p ${PID} > /dev/null;
do
    continue
done
