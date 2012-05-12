#!/bin/sh
python testshop/manage.py dumpdata --natural --exclude=contenttypes --exclude=auth --exclude=admin --exclude=sessions --indent=2 > data.json