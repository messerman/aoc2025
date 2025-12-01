#!/usr/bin/env bash
INPUT=$@
DATE=${INPUT:-$(TZ="America/New_York" date +"%d")}
if test -d ${DATE}; then
    echo "${DATE} already exists"
    exit 1
fi

mkdir -p ${DATE}
cp template.py ${DATE}/__main__.py
(cd ${DATE} && ln -s __main__.py solution.py)
touch ${DATE}/__init__.py
touch ${DATE}/sample.txt
touch ${DATE}/input.txt

cd ${DATE}
ln -s ../tools ./tools
git add .
