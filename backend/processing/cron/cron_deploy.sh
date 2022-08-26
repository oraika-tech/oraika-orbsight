#!/usr/bin/env bash

DIR_PATH=$(dirname "$0")
mkdir -p ~/.orbsight/cron/
sudo cp $DIR_PATH/active_observer_publisher.sh ~/.orbsight/cron/
sudo cp $DIR_PATH/observer_messager_job.crontab /etc/cron.d/observer_messager_job.crontab
