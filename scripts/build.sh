#!/bin/bash

set -eo pipefail

if [ -z "$1" ]
then
  echo 'Supply a version!'
  exit 1
fi

set -u
VERSION="$1"

cd "$(dirname "$0")/.."
PATH_REPO="$(pwd)"
rm -rf ./dist/

echo ''
echo '### TESTING PIP-INSTALL ###'
echo ''

PATH_VENV="/tmp/$(date +"%s")"
python3 -m virtualenv "$PATH_VENV" > /dev/null
cd /tmp
PYTHONPATH=''
source "${PATH_VENV}/bin/activate"
python3 -m pip install -e "$PATH_REPO" > /dev/null
download-mediawiki --help >/dev/null
deactivate
echo ' => OK'

echo ''
echo "### BUILDING VERSION: ${VERSION} ###"
echo ''

cd "$PATH_REPO"
rm -rf ./dist/*

echo "$VERSION" > VERSION
python3 -m pip install -r ./requirements_build.txt >/dev/null
python3 -m build
if [ -f "./dist/download-mediawiki-${VERSION}.tar.gz" ]
then
  mv "./dist/download-mediawiki-${VERSION}.tar.gz" "./dist/download_mediawiki-${VERSION}.tar.gz"
fi
rm -rf ./src/download_mediawiki.egg-info/

# python3 -m twine upload --repository pypi dist/*
