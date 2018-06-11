#!/usr/bin/env bash
echo "do on update"

TULIUS_BRANCH=$1
ROOTDIR=$PWD

echo "Stop existing compose"
cd scripts/tulius/$1
docker-compose down
cd $ROOTDIR

echo "Build docker container tulius_$1"
docker build -t tulius_$1 .

echo "Collect static"
docker run -v "$PWD/data/static":/opt/tulius/data/static \
    -e TULIUS_BRANCH="$1" \
    --net tuliusnet \
    tulius_$1 python manage.py collectstatic --noinput

echo "Migrate"
docker run \
    -e TULIUS_BRANCH="$1" \
    --net tuliusnet \
    tulius_$1 python manage.py migrate


echo "Run compose"

cd scripts/tulius/$1
docker-compose up -d --build --force-recreate
cd $ROOTDIR

echo "Done."
