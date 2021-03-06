#!/usr/bin/env bash
echo "do on update"

TULIUS_BRANCH=$1
ROOTDIR=$PWD

echo "Stop existing compose"
cd scripts/tulius/$1
docker-compose stop uwsgi
docker-compose exec celery python manage.py wait_celery
docker-compose down
docker system prune --force
docker rm -v $(docker ps --filter status=exited -q 2>/dev/null) 2>/dev/null
docker rmi $(docker images --filter dangling=true -q 2>/dev/null) 2>/dev/null
cd $ROOTDIR

echo "Pull docker container tulius_$1"
docker pull kozzztik/tulius:$1

echo "Collect static"
docker run -v "$PWD/data/static":/opt/tulius/data/static \
    -e TULIUS_BRANCH="$1" \
    --net tuliusnet \
    -v "/home/travis/$1/settings_production.py":/opt/tulius/settings_production.py \
    kozzztik/tulius:$1 python manage.py collectstatic --noinput

echo "Migrate"
docker run \
    -e TULIUS_BRANCH="$1" \
    --net tuliusnet \
    -v "/home/travis/$1/settings_production.py":/opt/tulius/settings_production.py \
    kozzztik/tulius:$1 python manage.py migrate


echo "Run compose"

cd scripts/tulius/$1
docker-compose up -d --build --force-recreate
cd $ROOTDIR

echo "Done."
