"""
Metadata download, update and storage.

WE assume that the 'id' in the ORF metadata is unique and use it.
"""

import logging
from datetime import date, timedelta
from pprint import pprint
import requests
from ..models import Oe1Program


broadcasts_link = 'http://audioapi.orf.at/oe1/json/current/broadcasts'

logger = logging.getLogger('orf_archive.oe1_download.metadata')


def retrieve_metadata():
    cur_bc = requests.get(broadcasts_link)
    broadcasts = cur_bc.json()
    metadata = []
    for broadcast in broadcasts:
        programs = broadcast.get('broadcasts')
        if programs:
            for program in programs:
                metadata.append(extract_program_details(program))
    return metadata


def extract_program_details(program):
    href = program.get('href')
    details = {}
    if href is None:
        logger.error('No detail link for program with id={}'.format(program.get('id')))
    else:
        try:
            req = requests.get(href)
            if req.status_code == 200:
                details = req.json()
        except:
            logger.error('Failed to retrieve program detail link: {}'.format(href))
    program.update(details)  # details keys are a superset of program keys
    #pprint(program)
    return program


def update_metadata(metadata):
    files_to_archive = []
    for program in metadata:
        if not program:  # should not be empty anyway
            logger.error('Program is empty!')
        else:
            orf_id = program.get('id')
            if orf_id is None:
                logger.error('No useful id in program!')
            else:
                store_metadata(orf_id, program)
                files_to_archive += get_filenames(program)
    return files_to_archive


def store_metadata(orf_id, program):
    t_day = program.get('broadcastDay')
    if t_day:
        t = str(t_day)
        t_day = '{}-{}-{}'.format(t[0:4], t[4:6], t[6:8])
    filenames = get_filenames(program)
    #print(orf_id, t_day, filenames, len(str(program)))
    old_objects = Oe1Program.objects.filter(orf_id=orf_id)
    if old_objects:
        old_program = old_objects[0]
        old_program.data = program
        old_program.t_day = t_day
        old_program.filenames = list(set(old_program.filenames + filenames))
        old_program.save()
    else:
        Oe1Program.objects.create(
            orf_id=orf_id,
            t_day=t_day,
            filenames=filenames,
            data=program,
        )


def get_filenames(program):
    streams = program.get('streams') or []
    return [stream.get('loopStreamId') for stream in streams if stream.get('loopStreamId')]


def get_latest_files():
    """
    Return all filenames of programs in the last 8 days.
    """
    t_0 = date.today() - timedelta(days=8)
    filenames = []
    for program_obj in Oe1Program.objects.filter(t_day__gte=t_0):
        filenames += program_obj.filenames
    return filenames
