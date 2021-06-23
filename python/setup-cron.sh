#!/bin/bash

cp /root/opt/kousotsu-cron /etc/cron.d/
chown root:root /etc/cron.d/kousotsu-cron
chmod 644 /etc/cron.d/kousotsu-cron

sed -e "s/#cron/cron/"  /etc/rsyslog.conf
service rsyslog start
service cron restart