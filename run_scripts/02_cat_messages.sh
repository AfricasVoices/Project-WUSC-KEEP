#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 02_cat_messages.sh <user> <data-root>"
    echo "Concatenates exports from multi-broadcast shows into single files. Single-broadcast shows are copied-through"
    exit
fi

USER=$1
DATA_DIR=$2

cd ../cat_traced_data

COPY_LIST=(
    "01 ELIMU"
    "03 RITA"
    "05 JOHN"
    "07 MARY"
    "09 GIRL"
    )

CAT_LIST=(
    "02a AKAI"  "02b AKAI"  "02 AKAI"
    "04a AKIRU" "04b AKIRU" "04 AKIRU"
    "06a EBEI"  "06b EBEI"  "06 EBEI"
    "08a AROP"  "08b AROP"  "08 AROP"
    "10a SHULE" "10b SHULE" "10 SHULE"
)

mkdir -p "$DATA_DIR/02 Raw Messages Concatenated"

for file in "${COPY_LIST[@]}"
do
    cp "$DATA_DIR/01 Raw Messages/$file.json" "$DATA_DIR/02 Raw Messages Concatenated/$file.json"
done

for i in $(seq 0 $((${#CAT_LIST[@]} / 3 - 1)))
do
    INPUT_1="${CAT_LIST[3 * i]}"
    INPUT_2="${CAT_LIST[3 * i + 1]}"
    OUTPUT="${CAT_LIST[3 * i + 2]}"

    sh docker-run.sh "$USER" "$DATA_DIR/01 Raw Messages/$INPUT_1.json" \
        "$DATA_DIR/01 Raw Messages/$INPUT_2.json" "$DATA_DIR/02 Raw Messages Concatenated/$OUTPUT.json"
done
