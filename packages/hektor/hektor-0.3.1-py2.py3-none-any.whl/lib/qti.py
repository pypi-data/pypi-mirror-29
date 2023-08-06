import base64
import re
import zipfile

from lxml import etree

import lib.generic


class QTIConverter(lib.generic.Converter):
    """ XLSConverter class (Currently raw xml input is not supported) """

    accepted_files = ('.zip', '.xml')

    def convert(self, filepath):
        with zipfile.ZipFile(filepath) as archive:
            data = dict(process_archive(archive))

        return give_me_structure(data)


file_regex = re.compile(
    r'(\d+)__(\d+)__(?P<data>results|qti|tst)_(?P<id>\d+).xml')
task_id_regex = re.compile(r'il_\d+_qst_(?P<task_id>\d+)')

tasks_path = ('./assessment/section')

users = './tst_active/row'
solutions = './tst_solutions/row[@question_fi="%s"]'

lecturer_xpath = ('./MetaData/Lifecycle/Contribute'
                  '[@Role="Author"]/Entity/text()')

types_xpath = ('./item/itemmetadata/qtimetadata/qtimetadatafield/'
               'fieldlabel[text()="QUESTIONTYPE"]/../fieldentry/text()')


def process_qti(tree, only_of_type=('assSourceCode',), **kwargs):
    tasks = tree.xpath(tasks_path)[0]

    titles = tasks.xpath('./item/@title')
    types = tasks.xpath(types_xpath)
    ids = [re.search(task_id_regex, ident).group('task_id')
           for ident in tasks.xpath('./item/@ident')]
    texts = ['\n'.join(flow.xpath('./material/mattext/text()'))
             for flow in tasks.xpath('./item/presentation/flow')]

    return {id: {'title': title, 'text': text, 'type': type}
            for id, type, title, text in zip(ids, types, titles, texts)
            if not only_of_type or type in only_of_type}


def process_users(results_tree):
    return [dict(row.attrib) for row in results_tree.xpath(users)]


def convert_code(text):
    return base64.b64decode(text).decode('utf-8')


def process_solutions(results_tree, task_id):
    return {row.attrib['active_fi']: convert_code(row.attrib['value1'])
            for row in results_tree.xpath(solutions % task_id)}


def process_results(tree, qti=(), **kwargs):
    questions = qti
    users = process_users(tree)
    id2user = {user['active_id']: user for user in users}
    for user in users:
        user['submissions'] = []
    for question in questions:
        solutions = process_solutions(tree, question)
        for user_id, solution in solutions.items():
            id2user[user_id]['submissions'].append({'type': question,
                                                    'code': solution,
                                                    'tests': {}})
    return users


def process_tst(tree):
    title = tree.xpath('./MetaData/General/Title/text()')
    lecturer = tree.xpath(lecturer_xpath)
    return {'exam': title[0], 'author': lecturer[0]}


def eval_file(archive, match, cache):
    funcname = 'process_' + match.group('data')
    with archive.open(match.string) as datafile:
        tree = etree.parse(datafile)
        return globals()[funcname](tree, **cache)


def process_archive(archive):
    files = {match.group('data'): match
             for match in (re.search(file_regex, name)
                           for name in archive.NameToInfo)
             if match}

    order = ('tst', 'qti', 'results')
    cache = {}

    for key in order:
        cache[key] = eval_file(archive, files[key], cache)

    return cache


def add_meta(base, data):
    base.update(data['tst'])


def add_tasks(base, data):
    base['tasks'] = list(data['qti'].values())


ignore_user_fields = ("user_fi",
                      "active_id",
                      "usr_id",
                      "anonymous_id",
                      "test_fi",
                      "lastindex",
                      "tries",
                      "submitted",
                      "submittimestamp",
                      "tstamp",
                      "user_criteria",)


def add_users(base, data):
    for userdata in data['results']:
        userdata['identifier'] = userdata['user_fi']
        userdata['username'] = userdata['user_fi']
        for field in ignore_user_fields:
            userdata.pop(field)
    base['students'] = data['results']


def give_me_structure(data):
    base = {}

    add_meta(base, data)
    add_tasks(base, data)
    add_users(base, data)

    return base
