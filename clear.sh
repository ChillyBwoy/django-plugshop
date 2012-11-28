#!/usr/bin/env bash
find . -name '*.pyc' -delete
rm -rf dist
rm -rf build
rm -rf django_plugshop.egg-info