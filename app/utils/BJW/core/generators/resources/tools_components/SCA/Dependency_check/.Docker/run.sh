#!/bin/sh

DC_VERSION="latest"
BIBIMBOB_DIRECTORY=$HOME/BIBIM
DC_DIRECTORY="$BIBIMBOB_DIRECTORY/OWASP-Dependency-Check"
DC_PROJECT="dependency-check scan: $(pwd)"
DATA_DIRECTORY="$DC_DIRECTORY/data"
CACHE_DIRECTORY="$DC_DIRECTORY/data/cache"

TARGET_DIRECTORY="$BIBIMBOB_DIRECTORY/target"
REPORT_DIRECTORY="$BIBIMBOB_DIRECTORY/report"
REPORT_FORMAT="JSON"

if [ ! -d "$DATA_DIRECTORY" ]; then
    echo "Initially creating persistent directory: $DATA_DIRECTORY"
    mkdir -p "$DATA_DIRECTORY"
fi
if [ ! -d "$CACHE_DIRECTORY" ]; then
    echo "Initially creating persistent directory: $CACHE_DIRECTORY"
    mkdir -p "$CACHE_DIRECTORY"
fi

docker pull owasp/dependency-check:$DC_VERSION

docker run --rm \
    -e user=$USER \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    --volume "$TARGET_DIRECTORY":/src:z \
    --volume "$DATA_DIRECTORY":/usr/share/dependency-check/data:z \
    --volume "$REPORT_DIRECTORY":/report:z \
    owasp/dependency-check:$DC_VERSION \
    --scan /src \
    --format "$REPORT_FORMAT" \
    --project "$DC_PROJECT" \
    --out /report