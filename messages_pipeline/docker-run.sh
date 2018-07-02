#!/bin/bash

set -e

if [ $# -ne 4 ]; then
    echo "Usage: sh docker-run.sh <user> <input-file> <output-file> <interface-dir>"
    exit
fi

USER=$1
INPUT_FILE=$2
OUTPUT_FILE=$3
INTERFACE_DIR=$4

# Build an image for this project, called "wusc-keep-messages".
docker build -t wusc-keep-messages .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" wusc-keep-messages)"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_FILE" "$container:/app/data/input.json"

# Run the image as a container.
docker start -a -i "$container"

# Copy the output data back out of the container
docker cp "$container:/app/data/output.json" "$OUTPUT_FILE"
docker cp "$container:/app/data/interface_export" "$INTERFACE_DIR"
