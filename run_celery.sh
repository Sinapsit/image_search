#!/bin/sh

sleep 5

cd project  
celery -A project worker -l info --beat