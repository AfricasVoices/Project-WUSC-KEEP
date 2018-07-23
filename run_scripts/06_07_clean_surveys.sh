#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 06_07_clean_surveys.sh <user> <data-root>"
    echo "Cleans demographic surveys, and exports codes to Coding CSVs for manual coding/verification."
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../survey_auto_code

SURVEYS=(
    "Demog Survey_ATA_Arabic"  arabic
    "Demog Survey_ATA_English" english
    "Demog Survey_ATA_Swahili" swahili
    "Demog Survey_ATA_Turkana" turkana

    "Demog Survey_BIBLIA_Swahili" swahili
    "Demog Survey_BIBLIA_Turkana" turkana
    )

for i in $(seq 0 $((${#SURVEYS[@]} / 2 - 1))) # for i in range(0, len(SHOWS) / 2)
do
    SURVEY="${SURVEYS[2 * i]}"
    LANGUAGE="${SURVEYS[2 * i + 1]}"

    echo "sh docker-run.sh" "$USER" \
        "\"$DATA_DIR/05 Raw Surveys/$SURVEY.json\"" "$LANGUAGE" "\"$DATA_DIR/06 Clean Surveys/$SURVEY.json\"" \
         coding-csv "\"$DATA_DIR/07 Coding CSVs/$SURVEY\""

    sh docker-run.sh "$USER" \
        "$DATA_DIR/05 Raw Surveys/$SURVEY.json" "$LANGUAGE" "$DATA_DIR/06 Clean Surveys/$SURVEY.json" \
         coding-csv "$DATA_DIR/07 Coding CSVs/$SURVEY"
done
