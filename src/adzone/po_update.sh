#!/bin/bash 

mkdir -p locale
django-admin.py makemessages --locale ru
