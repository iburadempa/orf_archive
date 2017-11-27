"""
Archive programs of Ö1 radio.

Ö1 radio is a radio station in Austria, see http://oe1.orf.at/ .
They have a 7 day archive for listening to past programs.
We download the programs (usually once a day) to build an archive
which goes back further in time.

We store the metadata in a Postgres database and the downloaded
mp3 files in a data storage directory.
"""

storage_path = '/srv/escape_supplement/orf_archive_files'
"""
Downloaded files will be stored below an served from this path.

django will need read and write permissions, including creation
of subdirectories.
"""
