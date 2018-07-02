#!/bin/bash

set -e

if [ $# -ne 5 ]; then
    echo "Usage: sh docker-run.sh <user> <input-file> <coding-mode> <coding-directory> <output-file>"
    exit
fi

USER=$1
INPUT_FILE=$2
CODING_MODE=$3
CODING_DIR=$4
OUTPUT_FILE=$5

# Build an image for this project, called "wusc-keep-merge-coded".
docker build -t wusc-keep-merge-coded .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" --env CODING_MODE="$CODING_MODE" wusc-keep-merge-coded)"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_FILE" "$container:/app/data/input.json"
docker cp "$CODING_DIR/." "$container:/app/data/coding"

# Run the image as a container.
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_FILE")"
docker cp "$container:/app/data/output.json" "$OUTPUT_FILE"
