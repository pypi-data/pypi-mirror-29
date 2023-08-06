#!/usr/local/bin/python3
""" a simple script that converts ilias exam output to readable json

usage: convert.py [-h] [-u USERNAMES] [-n NUMBER_OF_TASKS] INFILE OUTFILE

positional arguments:
  INFILE                Ilias exam data
  OUTFILE               Where to write the final file

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAMES, --usernames USERNAMES
                        a json dict matno -> email
  -n NUMBER_OF_TASKS, --NUMBER_OF_TASKS NUMBER_OF_TASKS
                        Where to write the final file


Author: Jan Maximilian Michal
Date: 30 March 2017
"""

import json
import os
import re
import urllib.parse
from collections import defaultdict, namedtuple

from xlrd import open_workbook

import lib.generic


class XLSConverter(lib.generic.Converter):
    """docstring for XLSConverter"""

    accepted_files = ('.xls',)

    def convert(self, filepath):
        return converter(filepath)


# one user has one submission (code) per task
# yes, I know it is possible to name match groups via (?P<name>) but
# I like this solution better since it gets the job done nicely
user_t = namedtuple('user_head', 'name matrikel_no')

# one task has a title and id and hpfly code
task_head_re = re.compile(r'^Quellcode Frage (?P<title>.*?) ?(\d{8})?$')

# nor parsing the weird mat no
matno_re = re.compile(r'^(?P<matrikel_no>\d{8})-(\d+)-(\d+)$')

TABWIDTH = 4


def converter(infile, usernames=None, number_of_tasks=0,):

    # Modify these iterators in order to change extraction behaviour

    def sheet_iter_meta(sheet):
        """ yield first and second col entry as tuple of (name, matnr) """
        for row in (sheet.row(i) for i in range(1, sheet.nrows)):
            match = re.search(matno_re, row[1].value)
            if match:
                yield row[0].value, match.group('matrikel_no')

    def sheet_iter_data(sheet):
        """ yields all source code titel and code tuples """
        def row(i):
            return sheet.row(i)
        for top, low in ((row(i), row(i + 1)) for i in range(sheet.nrows - 1)):
            if any(map(lambda c: c.ctype, top)) and 'Quell' in top[0].value:
                yield (' '.join(c.value for c in top),
                       ' '.join(c.value for c in low))

    # meta sheet contains ilias names usernames etc - data contains code
    meta, *data = open_workbook(infile, open(os.devnull, 'w')).sheets()

    # nice!
    name2mat = dict(sheet_iter_meta(meta))
    assert len(name2mat) == len(data), '{} names != {} sheets'.format(len(name2mat), len(data))  # noqa

    # from xls to lists and namedtuples
    # [ [user0, task0_h, code0, ..., taskn, coden ], ..., [...] ]
    root = []
    tasks = {}
    for user, sheet in zip(sheet_iter_meta(meta), data):
        root.append([user_t(*user)])
        for task, code in sheet_iter_data(sheet):
            task = re.search(task_head_re, task)
            task_title = task.group('title')
            tasks[task_title] = {
                'title': task_title,
                'type': 'SourceCode'
            }
            root[-1].append(task.group('title'))
            root[-1].append(urllib.parse
                            .unquote(code)
                            .replace('\t', ' ' * TABWIDTH))

    if number_of_tasks:
        for (user, *task_list) in sorted(root, key=lambda u: u[0].name):
            assert len(task_list) == number_of_tasks * 2

    mat_to_email = defaultdict(str)
    if usernames:
        with open(usernames) as data:
            mat_to_email.update(json.JSONDecoder().decode(data.read()))

    def get_username(user):
        if name2mat[user.name] in mat_to_email:
            return mat_to_email[name2mat[user.name]].split('@')[0]
        return ''.join(filter(str.isupper, user.name)) + name2mat[user.name]

    usernames = {user.name: get_username(user) for (user, *_) in root}

    return {
        'students': [{
            'fullname': user.name,
            'username': usernames[user.name],
            'email': mat_to_email[name2mat[user.name]],
            'identifier': name2mat[user.name],
            'submissions': [{
                "type": task,
                "code": code,
                "tests": {},
            } for task, code in zip(task_list[::2], task_list[1::2])]
        } for (user, *task_list) in sorted(root, key=lambda u: u[0].name)],
        'tasks': list(tasks.values())
    }


def write_to_file(json_dict, outfile):
    # just encode python style
    with open(outfile, "w") as out:
        json.dump(json_dict, out, indent=2)

    print("Wrote data to %s. Done." % outfile)
