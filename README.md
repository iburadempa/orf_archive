# orf_archive

A django app for download, display and mp3-serving of ORF
(Austrian public brodcaster) Ö1 (radio station) programs.

## Functionality

Ö1 radio is a radio station in Austria, see http://oe1.orf.at/ .
They have a 7 day archive for listening to past programs.
We download the programs (usually once a day) to build an
archive which goes back further in time.

We store the metadata in a Postgres database using django
and the downloaded mp3 files in a data storage directory.

A django webui allows to choose a day an displays the
programs of this day including mp3 download links.
It requires a login in the django project.

## Installation

  * you need a working django project with user authentication
  * pip install requests
  * copy directory orf_archive to your django project root
  * include orf_archive/urls.py from the project's urls.py
  * create a login (username/password) in your django project
    (any login will have access to the orf_archive)
  * add a cronjob or systemd.timer to your system which calls
    orf_archive/oe1_download/cronjob.sh once a day

It should run with python >= 3.4 (tested with 3.5).

## Download

Main repository: https://gitea.cosmopool.net/ibu/orf_archive
Alternative repo: https://github.com/iburadempa/orf_archive

## Alternative software

  * https://github.com/qubitstream/oe1_get/
  * https://github.com/nblock/feeds ; they have a spider for Ö1:
    https://github.com/nblock/feeds/blob/master/feeds/spiders/oe1_orf_at.py
