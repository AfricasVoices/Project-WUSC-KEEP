#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 09_merge_coded.sh <user> <data-root>"
    echo "Applies manually verified/assigned codes from coding csvs to the surveys."
    exit
fi

USER=$1
DATA_DIR=$2

cd ../survey_merge_coded

SURVEYS=(
    "Demog Survey_ATA_Arabic"
    "Demog Survey_ATA_English"
    "Demog Survey_ATA_Swahili"
    "Demog Survey_ATA_Turkana"

    "Demog Survey_BIBLIA_Swahili"
    "Demog Survey_BIBLIA_Turkana"
    )

for SURVEY in "${SURVEYS[@]}"
do
    echo "sh docker-run.sh" "$USER" "\"$DATA_DIR/06 Clean Surveys/$SURVEY.json\"" coding-csv \
        "\"$DATA_DIR/08 Coded Coding CSVs/$SURVEY\"" "\"$DATA_DIR/09 Coded Surveys/$SURVEY.json\""

    sh docker-run.sh "$USER" "$DATA_DIR/06 Clean Surveys/$SURVEY.json" coding-csv \
        "$DATA_DIR/08 Coded Coding CSVs/$SURVEY" "$DATA_DIR/09 Coded Surveys/$SURVEY.json"
done
