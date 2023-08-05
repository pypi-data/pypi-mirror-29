#!/usr/bin/env bash
#
# Wrapper script for Cloudtoken's AWS metadata endpoint.
# Brings up the 169.254.169.254 interface we require.
# We try to detect if we're running on MacOS or Linux.

INSTALL_DIR="$( cd "$( dirname "${BASH_SOURCE}" )" && pwd )"
PARAMS=( "$@" )

if [[ ${EUID} -ne 0 ]]; then
    echo "Please run as root. Exiting."
    exit 1
fi

if [[ $(uname) == 'Darwin' ]]; then
    INT='lo0'
else
    INT='lo'
fi

# Add ip aliases.
if [[ $(netstat -in | grep -c ${INT}) -gt 0 ]]; then
    echo -n "Configuring link-local address on ${INT}..."

    if [[ ${INT} == 'lo0' ]]
    then
        ifconfig ${INT} alias 169.254.169.254 255.255.255.255
    else
        ifconfig ${INT}:0 169.254.169.254 netmask 255.255.255.255 up
    fi

    if [[ $? -eq 0 ]]
    then
        echo "done."
    else
        echo "failed."
        exit 1
    fi
else
    echo "No loopback interface found. Exiting."
    exit 1
fi

# Now that the interfaces are up, run Cloudtoken and pass all the arguments.
${INSTALL_DIR}/cloudtoken.cmd "${PARAMS[@]}"

# Remove ip aliases.
if [[ ${INT} == 'lo0' ]]; then
    ifconfig ${INT} -alias 169.254.169.254
else
    ifconfig ${INT}:0 169.254.169.254 down
fi

unset INSTALL_DIR

