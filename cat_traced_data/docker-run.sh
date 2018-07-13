#!/bin/bash

set -e

if [ $# -ne 4 ]; then
    echo "Usage: sh docker-run.sh <user> <input-file-1> <input-file-2> <output-file>"
    exit
fi

USER=$1
INPUT_FILE_1=$2
INPUT_FILE_2=$3
OUTPUT_FILE=$4

# Build an image for this project, called "wusc-cat-traced-data".
docker build -t wusc-cat-traced-data .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" wusc-cat-traced-data)"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_FILE_1" "$container:/app/data/input_1.json"
docker cp "$INPUT_FILE_2" "$container:/app/data/input_2.json"

# Run the image as a container.
docker start -a -i "$container"

# Copy the output data back out of the container
docker cp "$container:/app/data/output.json" "$OUTPUT_FILE"
