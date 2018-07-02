#!/bin/bash

set -e

if [ $# -ne 6 ]; then
    echo "Usage: sh docker-run.sh <path_to_GitHub_key> <user> <input-file> <coding-mode> <coding-directory> <output-file>"
    exit
fi

GH_KEY=$1
USER=$2
INPUT_FILE=$3
CODING_MODE=$4
CODING_DIR=$5
OUTPUT_FILE=$6

# Copy key from the specified location to here, so that Docker can access it when building the image.
cp "$GH_KEY" .gh_rsa

function finish {
	# Delete the copy of the user's key we made in this directory.
    rm -f .gh_rsa
}
trap finish EXIT

# Build an image for this project, called "wusc-keep-merge-coded".
docker build -t wusc-keep-merge-coded .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" --env CODING_MODE="$CODING_MODE" wusc-keep-merge-coded)"

# Copy input data into the container
docker cp "$INPUT_FILE" "$container:/app/data/input.json"
docker cp "$CODING_DIR/." "$container:/app/data/coding"

# Run the image as a container.
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_FILE")"
docker cp "$container:/app/data/output.json" "$OUTPUT_FILE"
