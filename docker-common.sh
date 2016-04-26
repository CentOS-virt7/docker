#!/bin/sh
. /etc/sysconfig/docker
[ -e "${DOCKERBINARY}" ] || DOCKERBINARY=/usr/bin/docker-current
if [ ${DOCKERBINARY} == "/usr/bin/docker" ]; then
    echo "DOCKERBINARY has been set to an invalid value:" $DOCKERBINARY
    echo ""
    echo "Please set DOCKERBINARY to /usr/bin/docker-current or /usr/bin/docker-latest
by editing /etc/sysconfig/docker"
else
    exec ${DOCKERBINARY} "$@"
fi
