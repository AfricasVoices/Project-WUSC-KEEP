#!/usr/bin/env bash

set -e

if [ $# -ne 5 ]; then
    echo "Usage: sh 01_fetch_messages.sh <user> <echo-mobile-root> <echo-mobile-username> <echo-mobile-password> <data-root>"
    echo "Downloads all radio show answers from all shows."
    exit
fi

USER=$1
EM_DIR=$2
EM_USERNAME=$3
EM_PASSWORD=$4
DATA_DIR=$5

ORG="AVF - KEEP II"
VERBOSE="-v"

cd "$EM_DIR"

SHOWS=(
    # Start time                Cut-off time                Group name
    "2018-06-12T20:00:00+03:00" "2018-06-13T00:00:00+03:00" "01 ELIMU"
    "2018-06-14T09:00:00+03:00" "2018-06-14T12:00:00+03:00" "02a AKAI"
    "2018-06-15T20:00:00+03:00" "2018-06-16T00:00:00+03:00" "02b AKAI"

    "2018-06-19T20:00:00+03:00" "2018-06-20T00:00:00+03:00" "03 RITA"
    "2018-06-21T09:00:00+03:00" "2018-06-21T12:00:00+03:00" "04a AKIRU"
    "2018-06-22T20:00:00+03:00" "2018-06-23T00:00:00+03:00" "04b AKIRU"

    "2018-06-26T20:00:00+03:00" "2018-06-27T00:00:00+03:00" "05 JOHN"
    "2018-06-28T09:00:00+03:00" "2018-06-28T12:00:00+03:00" "06a EBEI"
    "2018-06-29T20:00:00+03:00" "2018-06-30T00:00:00+03:00" "06b EBEI"

    "2018-07-03T20:00:00+03:00" "2018-07-04T00:00:00+03:00" "07 MARY"
    "2018-07-05T09:00:00+03:00" "2018-07-05T12:00:00+03:00" "08a AROP"
    "2018-07-06T20:00:00+03:00" "2018-07-07T00:00:00+03:00" "08b AROP"

    "2018-07-10T20:00:00+03:00" "2018-07-11T00:00:00+03:00" "09 GIRL"
    "2018-07-12T09:00:00+03:00" "2018-07-12T12:00:00+03:00" "10a SHULE"
    "2018-07-13T20:00:00+03:00" "2018-07-14T00:00:00+03:00" "10b SHULE"
    )

for i in $(seq 0 $((${#SHOWS[@]} / 3 - 1))) # for i in range(0, len(SHOWS) / 3)
do
    START_TIME="${SHOWS[3 * i]}"
    END_TIME="${SHOWS[3 * i + 1]}"
    SHOW_NAME="${SHOWS[3 * i + 2]}"

    echo "pipenv run python messages_report.py" "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "\"$ORG\"" \
        "$START_TIME" "$END_TIME" "\"$DATA_DIR/00 UUIDs/phone_uuids.json\"" \
        "\"$DATA_DIR/00 UUIDs/message_uuids.json\"" "\"$DATA_DIR/01 Raw Messages/$SHOW_NAME.json\""

    pipenv run python messages_report.py "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "$ORG" \
        "$START_TIME" "$END_TIME" "$DATA_DIR/00 UUIDs/phone_uuids.json" \
        "$DATA_DIR/00 UUIDS/message_uuids.json" "$DATA_DIR/01 Raw Messages/$SHOW_NAME.json"
done
