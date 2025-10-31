#!/bin/bash

set -e

cd "$(dirname "$0")/.."

PYTHONPATH=''

echo ''
echo 'FUNCTIONAL TEST'
echo ''

DUMP_DIR="/tmp/$(date +'%s')"
export TEST=1
python3 src/download_mediawiki/ --url 'https://wiki.nftables.org/wiki-nftables' --convert-to-md --out-dir "$DUMP_DIR"

ls -l "$DUMP_DIR"

if [ ! -f "${DUMP_DIR}/overview.json" ]
then
  echo 'OVERVIEW missing'
  exit 1
fi

if [ ! -d "${DUMP_DIR}/0" ]
then
  echo 'NAMESPACE-DIR missing'
  exit 1
fi

ls -l "${DUMP_DIR}/0"

if [ ! -f "${DUMP_DIR}/0/11.mw" ]
then
  echo 'PAGE-FILE (.mw) missing'
  exit 1
fi

if [ ! -f "${DUMP_DIR}/0/11.md" ]
then
  echo 'PAGE-FILE (.md) missing'
  exit 1
fi

rm -r "$DUMP_DIR"
