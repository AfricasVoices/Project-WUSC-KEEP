#!/usr/bin/env bash

set -e

if [ $# -ne 5 ]; then
    echo "Usage: sh 05_fetch_surveys.sh <user> <echo-mobile-root> <echo-mobile-username> <echo-mobile-password> <data-root>"
    echo "Downloads all demographic surveys."
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

SURVEYS=(
    "Demog Survey_ATA_Arabic"
    "Demog Survey_ATA_English"
    "Demog Survey_ATA_Swahili"
    "Demog Survey_ATA_Turkana"
    )

for SURVEY in "${SURVEYS[@]}"
do
    echo "pipenv run python survey_report.py" "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "\"$ORG\"" \
        "\"$SURVEY\"" "\"$DATA_DIR/00 UUIDs/phone_uuids.json\"" "\"$DATA_DIR/05 Raw Surveys/$SURVEY.json\""

    pipenv run python survey_report.py "$VERBOSE" "$USER" "$EM_USERNAME" "$EM_PASSWORD" "$ORG" \
        "$SURVEY" "$DATA_DIR/00 UUIDs/phone_uuids.json" "$DATA_DIR/05 Raw Surveys/$SURVEY.json"
done
