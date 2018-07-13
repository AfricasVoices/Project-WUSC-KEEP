#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 01_fetch_messages.sh <echo-mobile-root> <data-root>"
    echo "Writes empty UUID tables for phone numbers and messages."
    exit
fi

EM_DIR=$1
DATA_DIR=$2

mkdir -p "$DATA_DIR/00 UUIDs"

echo "{}" >"$DATA_DIR/00 UUIDs/phone_uuids.json"
echo "{}" >"$DATA_DIR/00 UUIDs/message_uuids.json"
