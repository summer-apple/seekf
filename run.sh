#!/bin/bash

pid=`pidof uwsgi | awk '{print$1}'`
echo "old uwsgi pid is:$pid"

pkill -9 uwsgi

uwsgi -d /var/log/uwsgi.log --ini /root/sites/seekf/conf/uwsgi.ini
service nginx restart

newpid=`pidof uwsgi | awk '{print$1}'`
echo "new uwsgi pid is:$newpid"