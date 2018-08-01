#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 07_08_join_messages_surveys.sh <user> <data-root>"
    echo "Joins messages and demographic surveys on phone id, and produces CSV files for analysis"
    exit
fi

USER=$1
DATA_ROOT=$2

cd ../join_messages_surveys

mkdir -p "$DATA_ROOT/10 Analysis Data"
mkdir -p "$DATA_ROOT/11 Analysis CSVs"

SHOWS=(
    "01 ELIMU" ATA
    "02 AKAI" BIBLIA

    "03 RITA" ATA
    "04 AKIRU" BIBLIA

    "05 JOHN" ATA
    "06 EBEI" BIBLIA

    "07 MARY" ATA
    "08 AROP" BIBLIA

    "09 GIRL" ATA
    "10 SHULE" BIBLIA
    )

for i in $(seq 0 $((${#SHOWS[@]} / 2 - 1)))
do
    SHOW="${SHOWS[2 * i]}"
    STATION="${SHOWS[2 * i + 1]}"

    if [ "$STATION" == ATA ]
    then
        LANGUAGES=("Arabic" "English" "Swahili" "Turkana")
    else
        LANGUAGES=("Swahili" "Turkana")
    fi

    cp "$DATA_ROOT/03 Clean Messages/$SHOW.json" "$DATA_ROOT/10 Analysis Data/$SHOW.json"

    for LANGUAGE in "${LANGUAGES[@]}"
    do
        echo "Joining $SHOW.$STATION.$LANGUAGE"

        sh docker-run.sh "$USER" "$DATA_ROOT/10 Analysis Data/$SHOW.json" \
            "$DATA_ROOT/09 Coded Surveys/Demog Survey_${STATION}_$LANGUAGE.json" \
            "$DATA_ROOT/10 Analysis Data/$SHOW.json" "$DATA_ROOT/11 Analysis CSVs/$SHOW.csv"
    done
done
