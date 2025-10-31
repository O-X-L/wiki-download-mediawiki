#!/bin/bash

set -e

cd "$(dirname "$0")/.."

PYTHONPATH=''

echo ''
echo 'FUNCTIONAL TEST'
echo ''

python3 src/download_mediawiki/ --url 'https://wiki.nftables.org/wiki-nftables' --convert-to-md
