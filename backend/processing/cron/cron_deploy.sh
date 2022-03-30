#!/usr/bin/env bash

mkdir -p ~/.obsights/cron/
sudo cp obsights/processing/cron/active_observer_publisher.sh ~/.obsights/cron/
sudo cp obsights/processing/cron/observer_messager_job.crontab /etc/cron.d/observer_messager_job.crontab
