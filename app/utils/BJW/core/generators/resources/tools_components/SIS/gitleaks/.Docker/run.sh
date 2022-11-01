#!/bin/sh

VERSION="latest"
BIBIMBOB_DIRECTORY=$HOME/BIBIM
TARGET_DIRECTORY="$BIBIMBOB_DIRECTORY/target"
REPORT_DIRECTORY="$BIBIMBOB_DIRECTORY/report"
REPORT_FORMAT="json"
REPORT_FILE_NAME="sis-gitleaks-report.$REPORT_FORMAT"

if [ ! -d "$TARGET_DIRECTORY" ]; then
    echo "Initially creating persistent directory: $TARGET_DIRECTORY"
    mkdir -p "$TARGET_DIRECTORY"
fi
if [ ! -d "$REPORT_DIRECTORY" ]; then
    echo "Initially creating persistent directory: $REPORT_DIRECTORY"
    mkdir -p "$REPORT_DIRECTORY"
fi

docker build --tag gitleaks:$VERSION .

docker run --rm  \
    --volume "$TARGET_DIRECTORY":/src:z \
    --volume "$REPORT_DIRECTORY":/report:z \
    gitleaks:$VERSION detect \
    --no-git \
    --source /src \
    --report-format "$REPORT_FORMAT" \
    --report-path /report/"$REPORT_FILE_NAME"