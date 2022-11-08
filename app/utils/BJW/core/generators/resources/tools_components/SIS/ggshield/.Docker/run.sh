#!/bin/sh

if [ $# -eq "0" ]; then
    echo "Gitguardian API key is required"
    echo "syntax: $0 <token>"
    exit 1
fi

VERSION="latest"
BIBIMBOB_DIRECTORY=$HOME/BIBIM
TARGET_DIRECTORY="$BIBIMBOB_DIRECTORY/target"
REPORT_DIRECTORY="$BIBIMBOB_DIRECTORY/report"
REPORT_FORMAT="json"
REPORT_FILE_NAME="sis-ggshield-report.$REPORT_FORMAT"
GITGUARDIAN_API_KEY=$1

if [ ! -d "$TARGET_DIRECTORY" ]; then
    echo "Initially creating persistent directory: $TARGET_DIRECTORY"
    mkdir -p "$TARGET_DIRECTORY"
fi
if [ ! -d "$REPORT_DIRECTORY" ]; then
    echo "Initially creating persistent directory: $REPORT_DIRECTORY"
    mkdir -p "$REPORT_DIRECTORY"
fi

docker build --tag ggshield:$VERSION .

docker run --rm \
    --env GITGUARDIAN_API_KEY=$GITGUARDIAN_API_KEY \
    --volume "$TARGET_DIRECTORY":/src:z \
    --volume "$REPORT_DIRECTORY":/report:z \
    ggshield:$VERSION secret scan \
    --json \
    path . \
    --recursive -y > $REPORT_DIRECTORY/$REPORT_FILE_NAME