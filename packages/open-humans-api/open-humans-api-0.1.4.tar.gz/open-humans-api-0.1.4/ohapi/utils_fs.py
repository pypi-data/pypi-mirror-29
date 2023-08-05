"""
Utility functions to sync and work with Open Humans data in a local filesystem.
"""
import csv
import hashlib
import logging
import os
import re

import arrow
from humanfriendly import format_size, parse_size
import requests


MAX_FILE_DEFAULT = parse_size('128m')


def guess_tags(filename):
    tags = []
    if filename.endswith('.vcf' or '.vcf.gz' or '.vcf.bz2'):
        tags.append('vcf')
    if filename.endswith('.json' or '.json.gz' or '.json.bz2'):
        tags.append('json')
    if filename.endswith('.csv' or '.csv.gz' or '.csv.bz2'):
        tags.append('csv')
    return tags


def characterize_local_files(filedir, max_bytes=MAX_FILE_DEFAULT):
    """
    Collate local file info as preperation for Open Humans upload.

    Note: Files with filesize > max_bytes are not included in returned info.
    """
    file_data = {}
    logging.info('Characterizing files in {}'.format(filedir))
    for filename in os.listdir(filedir):
        filepath = os.path.join(filedir, filename)
        file_stats = os.stat(filepath)
        creation_date = arrow.get(file_stats.st_ctime).isoformat()
        file_size = file_stats.st_size
        if file_size <= max_bytes:
            file_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    file_md5.update(chunk)
            md5 = file_md5.hexdigest()
            file_data[filename] = {
                'tags': guess_tags(filename),
                'description': '',
                'md5': md5,
                'creation_date': creation_date,
            }
    return file_data


def validate_metadata(target_dir, metadata):
    """
    Check that the files listed in metadata exactly match files in target dir.
    """
    file_list = os.listdir(target_dir)
    for filename in file_list:
        if filename not in metadata:
            return False
    for filename in metadata:
        if filename not in file_list:
            return False
    return True


def load_metadata_csv(input_filepath):
    """
    Return dict of metadata.

    Format is either dict (filenames are keys) or dict-of-dicts (project member
    IDs as top level keys, then filenames as keys).
    """
    with open(input_filepath) as f:
        csv_in = csv.reader(f)
        header = csv_in.next()
        try:
            tags_idx = header.index('tags')
        except ValueError:
            tags_idx = None
        if header[0] == 'project_member_id':
            metadata = {}
            for row in csv_in:
                if row[0] not in metadata:
                    metadata[row[0]] = {}
                if row[1] == 'None' and all([x == 'NA' for x in row[2:]]):
                    continue
                metadata[row[0]][row[1]] = {
                    header[i]: row[i] for i in range(2, len(header)) if
                    i != tags_idx
                }
                metadata[row[0]][row[1]]['tags'] = [t.strip() for t in
                                                    row[tags_idx].split(',') if
                                                    t.strip()]
        elif header[0] == 'filename':
            metadata = {}
            for row in csv_in:
                if row[0] == 'None' and [x == 'NA' for x in row[1:]]:
                    break
                metadata[row[0]] = {
                    header[i]: row[i] for i in range(1, len(header)) if
                    i != tags_idx
                }
                metadata[row[0]]['tags'] = [t.strip() for t in
                                            row[tags_idx].split(',') if
                                            t.strip()]
    return metadata


def mk_metadata_csv(filedir, outputfilepath, max_bytes=MAX_FILE_DEFAULT):
    with open(outputfilepath, 'w') as outputfile:
        csv_out = csv.writer(outputfile)
        subdirs = [os.path.join(filedir, i) for i in os.listdir(filedir) if
                   os.path.isdir(os.path.join(filedir, i))]
        if subdirs:
            logging.info('Making metadata for subdirs of {}'.format(filedir))
            if not all([re.match('^[0-9]{8}$', os.path.basename(d))
                        for d in subdirs]):
                raise ValueError("Subdirs not all project member ID format!")
            csv_out.writerow(['project_member_id', 'filename', 'tags',
                              'description', 'md5', 'creation_date'])
            for subdir in subdirs:
                file_info = characterize_local_files(
                    filedir=subdir, max_bytes=max_bytes)
                proj_member_id = os.path.basename(subdir)
                if not file_info:
                    csv_out.writerow([proj_member_id, 'None',
                                      'NA', 'NA', 'NA', 'NA'])
                    continue
                for filename in file_info:
                    csv_out.writerow([proj_member_id,
                                      filename,
                                      ', '.join(file_info[filename]['tags']),
                                      file_info[filename]['description'],
                                      file_info[filename]['md5'],
                                      file_info[filename]['creation_date'],
                                      ])
        else:
            csv_out.writerow(['filename', 'tags',
                              'description', 'md5', 'creation_date'])
            file_info = characterize_local_files(
                filedir=filedir, max_bytes=max_bytes)
            for filename in file_info:
                csv_out.writerow([filename,
                                  ', '.join(file_info[filename]['tags']),
                                  file_info[filename]['description'],
                                  file_info[filename]['md5'],
                                  file_info[filename]['creation_date'],
                                  ])


def download_file(download_url, target_filepath, max_bytes=MAX_FILE_DEFAULT):
    """
    Download a file.
    """
    response = requests.get(download_url, stream=True)
    size = int(response.headers['Content-Length'])

    if size > max_bytes:
        logging.info('Skipping {}, {} > {}'.format(
            target_filepath, format_size(size), format_size(max_bytes)))
        return

    logging.info('Downloading {} ({})'.format(
        target_filepath, format_size(size)))

    if os.path.exists(target_filepath):
        stat = os.stat(target_filepath)
        if stat.st_size == size:
            logging.info('Skipping, file exists and is the right '
                         'size: {}'.format(target_filepath))
            return
        else:
            logging.info('Replacing, file exists and is the wrong '
                         'size: {}'.format(target_filepath))
            os.remove(target_filepath)

    with open(target_filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    logging.info('Download complete: {}'.format(target_filepath))


def read_id_list(filepath):
    if not filepath:
        return None
    id_list = []
    with open(filepath) as f:
        for line in f:
            line = line.rstrip()
            if not re.match('^[0-9]{8}$', line):
                raise('Each line in whitelist or blacklist is expected '
                      'to contain an eight digit ID, and nothing else.')
            else:
                id_list.append(line)
    return id_list
