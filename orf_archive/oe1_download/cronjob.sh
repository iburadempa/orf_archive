#!/bin/bash

. /srv/escape/escape/bin/activate
DJANGO_SETTINGS_MODULE="escape.settings.production" /srv/escape/escape/repo/manage.py run_orf_oe1_download
