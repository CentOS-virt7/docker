#!/bin/sh
. /etc/sysconfig/docker
[ -e "${DOCKERBINARY}" ] || DOCKERBINARY=/usr/bin/docker-current
exec ${DOCKERBINARY} $@
