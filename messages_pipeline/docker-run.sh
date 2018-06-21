#!/bin/bash

set -e

if [ $# -ne 5 ]; then
    echo "Usage: sh docker-run.sh <path_to_GitHub_key> <user> <input-file> <output-file> <interface-dir>"
    exit
fi

GH_KEY=$1
USER=$2
INPUT_FILE=$3
OUTPUT_FILE=$4
INTERFACE_DIR=$5

# Copy key from the specified location to here, so that Docker can access it when building the image.
cp "$GH_KEY" .gh_rsa

function finish {
	# Delete the copy of the user's key we made in this directory.
    rm -f .gh_rsa
}
trap finish EXIT

# Build an image for this project, called "wusc-keep".
docker build -t wusc-keep .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" wusc-keep)"

# Copy input data into the container
docker cp "$INPUT_FILE" "$container:/app/data/input.json"

# Run the image as a container.
docker start -a -i "$container"

# Copy the output data back out of the container
docker cp "$container:/app/data/output.json" "$OUTPUT_FILE"
docker cp "$container:/app/data/interface_export" "$INTERFACE_DIR"
