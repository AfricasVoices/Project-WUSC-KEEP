#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 03_04_clean_messages.sh <user> <data-root>"
    echo "Cleans radio show answers, and exports to CSVs for analysis."
    exit
fi

USER=$1
DATA_DIR=$2

ORG="AVF - KEEP II"

cd ../messages_pipeline

mkdir -p "$DATA_DIR/03 Clean Messages"
mkdir -p "$DATA_DIR/04 Message CSVs"

SHOWS=(
    "01 ELIMU"
    "02 AKAI"
    "03 RITA"
    "04 AKIRU"
    "05 JOHN"
    "06 EBEI"
    "07 MARY"
    "08 AROP"
    "09 GIRL"
    "10 SHULE"
    )

for SHOW in "${SHOWS[@]}"
do
    echo "sh docker-run.sh" "$USER" "$DATA_DIR/02 Raw Messages Concatenated/$SHOW.json" \
        "$DATA_DIR/03 Clean Messages/$SHOW.json" "$DATA_DIR/04 Message CSVs/$SHOW.csv"

    sh docker-run.sh "$USER" "$DATA_DIR/02 Raw Messages Concatenated/$SHOW.json" \
        "$DATA_DIR/03 Clean Messages/$SHOW.json" "$DATA_DIR/04 Message CSVs/$SHOW.csv"
done
