#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

DOCKERFILE=$DIR"/build/Dockerfile"
WORK="work"
DEPLOY="deploy"
CLEAN="true"
DOCKER="docker"
CONTAINER_NAME="sub-gen"

CONTAINER_EXISTS=$(${DOCKER} ps -a --filter name="${CONTAINER_NAME}" -q)
CONTAINER_RUNNING=$(${DOCKER} ps --filter name="${CONTAINER_NAME}" -q)
if [ "${CONTAINER_RUNNING}" != "" ]; then
	echo "Stopping container"
    ${DOCKER} stop ${CONTAINER_NAME}
fi
if [ "${CONTAINER_EXISTS}" != "" ]; then
    echo "Removing container"
    ${DOCKER} rm ${CONTAINER_NAME}
fi

for FOLDER in $WORK $DEPLOY; do
    if [ -d $FOLDER ]; then
        if [ $CLEAN == "true" ]; then
            rm -rf $FOLDER
        fi
    fi
    mkdir $FOLDER
done

${DOCKER} build -t ${CONTAINER_NAME} -f $DOCKERFILE .
${DOCKER} run \
 --name ${CONTAINER_NAME} \
 -e "OPTIMIZE=False" \
 -v $DIR/${WORK}:/sub-gen/${WORK} \
 -v $DIR/${DEPLOY}:/sub-gen/${DEPLOY} \
 ${CONTAINER_NAME}
