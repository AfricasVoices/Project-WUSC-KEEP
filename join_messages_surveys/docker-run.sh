#!/bin/bash

set -e

IMAGE_NAME=wt-join-messages-surveys

# Check that the correct number of arguments were provided.
if [ $# -ne 5 ]; then
    echo "Usage: sh docker-run.sh <user> <messages-input-file> <demog-input-file> <output-file> <output-csv>"
    exit
fi

# Assign the program arguments to bash variables.
USER=$1
INPUT_MESSAGES=$2
INPUT_DEMOG=$3
OUTPUT_JSON=$4
OUTPUT_CSV=$5

# Build an image for this pipeline stage.
docker build -t "$IMAGE_NAME" .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" "$IMAGE_NAME")"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_MESSAGES" "$container:/data/messages-input.json"
docker cp "$INPUT_DEMOG" "$container:/data/demog-input.json"

# Run the container
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_JSON")"
docker cp "$container:/data/output.json" "$OUTPUT_JSON"

mkdir -p "$(dirname "$OUTPUT_CSV")"
docker cp "$container:/data/output.csv" "$OUTPUT_CSV"
