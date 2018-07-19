#!/bin/bash

set -e

if [ $# -ne 6 ]; then
    echo "Usage: sh docker-run.sh <user> <input-file> <language> <output-file> <coding-mode> <coding-directory>"
    exit
fi

USER=$1
INPUT_FILE=$2
LANGUAGE=$3
OUTPUT_FILE=$4
CODING_MODE=$5
CODING_DIR=$6

# Build an image for this project, called "wusc-keep-auto-code".
docker build -t wusc-keep-auto-code .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" --env LANGUAGE="$LANGUAGE" --env CODING_MODE="$CODING_MODE" wusc-keep-auto-code)"

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
mkdir -p "$(dirname "$OUTPUT_FILE")"
docker cp "$container:/app/data/output.json" "$OUTPUT_FILE"

mkdir -p "$CODING_DIR"
docker cp "$container:/app/data/coding/." "$CODING_DIR"
