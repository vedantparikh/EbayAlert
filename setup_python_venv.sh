#!/usr/bin/env bash

BASEDIR=$(dirname $0)
echo "Script location: ${BASEDIR}"
PYTHON_BIN=python3.7
VIRTUALENV=.venv
PIP="${BASEDIR}/${VIRTUALENV}/bin/pip"

"${PYTHON_BIN}" -m venv "${VIRTUALENV}"
"${PIP}" install pip --upgrade
"${PIP}" install -r ${BASEDIR}/src/python/requirements.txt