import argparse
import base64
import functools
import getpass
import json
import logging
import os
from typing import Any, Callable, Dict, List, Sequence, Union

from cryptography.fernet import Fernet
from xkcdpass import xkcd_password as xp

from lib import Converter


# ============================== =- Logging -= ============================== #
def setup_logging():
    ''' Make the logger globally available by hide intermediate handler,
    filters and formatter variables '''
    global log

    level = logging.DEBUG if args.verbose else logging.INFO

    log = logging.getLogger(__name__)
    log.setLevel(level)

    # create console handler and formatter
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    # add formatter to console handler
    console.setFormatter(formatter)
    log.addHandler(console)


# ============================= =- argparse -= ============================== #
def setup_argparse():
    global args

    def file_exists(parser, filepath: str) -> str:
        if not os.path.isfile(filepath):
            parser.error('Not a file %s' % filepath)
        return filepath

    parser = argparse.ArgumentParser()

    # General purpose arguments
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='enable verbose logging (Level: DEBUG)')

    # Input output files
    parser.add_argument(
        'input',
        metavar='DATA',
        type=lambda f: file_exists(parser, f),
        help='an Ilias course export in .zip or .xls format')
    parser.add_argument(
        'output',
        metavar='OUTFILE',
        help='destination of converter output (JSON)')

    # Post-processor flags
    remove_personal = parser.add_mutually_exclusive_group()
    remove_personal.add_argument(
        '-e', '--encrypt',
        action='store_true',
        help='''strip all personal information and provide decryption key
                (AES 128-bit, CBC mode, PKCS7 for padding, HMAC with SHA-256
                for integrity)'''
    )
    remove_personal.add_argument(
        '-d', '--decrypt',
        action='store_true',
        help='Reverse previous AES encryption.')
    remove_personal.add_argument(
        '-a', '--anonymous',
        action='store_true',
        help='replace personal information and create a reversing table')
    parser.add_argument(
        '-t', '--personal-secret-table',
        help='where to store personal information (CSV)',
    )
    parser.add_argument(
        '-m', '--add-meta',
        action='store_true',
        help='add meta information (lecturer, course title)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        default=True,
        help='asserts that output data will be in a certain format'
    )
    parser.add_argument(
        '-r', '--readable-code',
        action='store_true',
        default=True,
        help='make student code readable by inserting artificial line breaks')

    args = parser.parse_args()

    if args.anonymous != (args.personal_secret_table is not None):
        parser.error('Please specify where to write the mapping (see -t)')


# ========================== =- General Purpose -= ========================== #
def compose(*functions: Sequence[Callable]) -> Callable:
    """ Standard function composition. Takes a Sequence of functions [f, g, h, ...]
    and returns the composite function i(x) = f(g(h(x))). There are no checks
    that validate if domain and image of these functions are compatible. """
    return functools.reduce(lambda f,
                            g: lambda x: f(g(x)),
                            functions,
                            lambda x: x)


def abort(message='Bye.'):
    ''' In case anything goes wrong. Basically a dump wrapper around exit '''
    log.info(message)
    exit(1)


# ========================== =- Post processors -= ========================== #
def student_replacer(processor):
    ''' A simple decorator that is used to remove students and put them back in
    when the preprocessor is dome with them'''

    @functools.wraps(processor)
    def processor_closure(structured_data: Dict[str, Any]) -> Dict[str, Any]:
        students = structured_data.pop('students')
        students_replacement = processor(students)
        structured_data['students'] = students_replacement
        return structured_data

    return processor_closure


def do_add_meta(structured_data: Dict[str, Any]) -> Dict[str, Any]:
    ''' Asks the user for metadata about the exam '''
    structured_data['author'] = input('[Q] author: ')
    structured_data['exam'] = input('[Q] course title: ')
    return structured_data


def do_verify(structured_data: Dict[str, Any]) -> Dict[str, Any]:
    ''' The is the testable specification of the format that is output by
    hector. Since multiple formats are compiled into this one verification is
    on by default. The impact on performance is neglectable. '''
    def assert_submission(submission):
        assert 'code' in submission, 'A submission needs code'
        assert type(submission['code']) in [str, list], 'Code is readable'
        assert 'type' in submission, 'A submission has to be of some type'
        assert 'tests' in submission, 'A tests dict has to be present.'

    def assert_student(student):
        log.debug('asserting %s (%d)' % (student['fullname'],
                                         len(student['submissions'])))
        assert 'fullname' in student, 'Student needs a name %s' % student
        assert 'identifier' in student, 'Student needs a unique identifier'
        assert 'username' in student, 'Student needs a unique username'

    def base_assert():
        assert 'students' in structured_data, 'No students found'
        assert 'tasks' in structured_data, 'No tasks found'

    try:
        base_assert()
        students = structured_data['students']
        number_of_submissions = len(structured_data['tasks'])
        for student in students:

            try:
                assert_student(student)
                assert number_of_submissions == len(student['submissions']), \
                    '%s does not have enough submissions' % student['fullname']
                for submission in student['submissions']:

                    try:
                        assert_submission(submission)
                    except AssertionError as err:
                        log.warn(err)

            except AssertionError as err:
                log.warn(err)

    except AssertionError as err:
        log.warn(err)

    return structured_data


@student_replacer
def do_readable_code(students: Dict[str, Union[str, List]]):
    for student in students:
        for submission in student['submissions']:
            submission['code'] = submission['code'].split('\n')
    return students


@student_replacer
def do_anonymous(students: Dict[str, Union[str, List]]):
    ''' Recreates most of the data and includes fields over a whitelist
    therefore ensuring that no personal information remains in the data '''
    DELIMITER = '-'
    wordfile = xp.locate_wordfile()
    words = xp.generate_wordlist(wordfile=wordfile,
                                 min_length=7,
                                 max_length=7)

    def get_random_xkcd_identifier():
        return xp.generate_xkcdpassword(words, numwords=2, delimiter=DELIMITER)

    reverser = {get_random_xkcd_identifier(): s for s in students}
    students_anonymous = [{
        'fullname': ' '.join(w[0].capitalize() + w[1:]
                             for w in r.split(DELIMITER)),
        'identifier': r,
        'username': r,
        'submissions': student['submissions']
    } for r, student in zip(reverser, students)]

    with open(args.personal_secret_table, 'w') as out:
        print('key, previous identifier, fullname', file=out)
        print('\n'.join('%s %s %s' % (anonymous_key,
                                      data['identifier'],
                                      data['fullname'])
                        for anonymous_key, data in reverser.items()), file=out)

    return students_anonymous


@student_replacer
def do_encrypt(students):

    # Init Crypto. See the module documentation on what actually happens here,
    # then read all about those methods and then go study number theory. Never
    # roll your own custom crypto ;-)
    key = Fernet.generate_key()
    aes = Fernet(key)

    def encrypt(clear: str) -> str:
        return base64.b64encode(aes.encrypt(clear.encode())).decode('utf-8')

    output_the_key_to_the_user(key)
    return transform(students, encrypt)


@student_replacer
def do_decrypt(students):

    def decrypt(cipher: str) -> str:
        return aes.decrypt(base64.b64decode(cipher.encode())).decode('utf-8')

    try:
        key = getpass.getpass('[Q] Give me the decryption key: ')
        aes = Fernet(key)

        return transform(students, decrypt)
    except Exception as err:
        abort('Your key is bad (%s).' % err)


# ======================= =- Post processor helper -= ======================= #
def transform(students, function):
    return [
        {'fullname': function(student['fullname']),
         'identifier': function(student['identifier']),
         'username': function(student['username']),
         'submissions': student['submissions']} for student in students
    ]


def output_the_key_to_the_user(key: bytes):

    def to_file(filepath: str):
        with open(filepath, 'wb') as file:
            file.write(key)
        log.info('Key written to %s. Keep it safe.', filepath)

    def to_stdout():
        print('Encrypted and signed. Key this key safe or bad things happen')
        print('   --------->> %s <<---------   ' % key.decode('latin-1'))

    output = input('[Q] The data has been encrypted. ' +
                   'Where should I put the key? (stdout) ') or 'stdout'

    if output == 'stdout':
        to_stdout()

    elif not os.path.exists(output):
        to_file(output)

    elif os.path.isfile(output):
        confirm = input('[Q] File exists. Want to override? (Y/n)') or 'y'
        if confirm.lower().startswith('y'):
            to_file(output)
        else:
            abort('No data was written. Bye.')

    else:
        log.error('I cannot write to %s.', output)
        abort()


def get_active_postprocessors():
    postprocessor_order = (
        do_add_meta,
        do_verify,
        do_readable_code,
        do_anonymous,
        do_encrypt,
        do_decrypt
    )

    return (p for p in postprocessor_order
            if getattr(args, p.__name__.split('do_')[1]))


# ============================== =- Hektor -= =============================== #
def _preprocessing(filepath: str) -> str:
    return filepath


def _processing(filepath: str) -> Dict[str, Any]:
    ''' Find the first apropriate converter and run pass it the path to the
    datafile. '''
    try:
        return next(converter().convert(filepath)
                    for converter in Converter.implementations()
                    if converter.accept(filepath))
    except StopIteration as err:
        log.error('No suitable converter found. Accepting only %s' %
                  ', '.join(f
                            for c in Converter.implementations()
                            for f in c.accepted_files))
        abort('Program stopped prematurely. No data was written. Bye.')


def _postprocessing(structured_data: Dict[str, Any]) -> Dict[str, Any]:
    return compose(*get_active_postprocessors())(structured_data)


def main():
    setup_argparse()
    setup_logging()

    log.debug('Active post processors %s', list(get_active_postprocessors()))

    processing = compose(_postprocessing, _processing, _preprocessing)
    data = processing(args.input)

    destination = args.output.split('.json')[0] + '.json'
    with open(destination, 'w') as output:
        json.dump(data, output, indent=2, sort_keys=True)

    log.info('Wrote exam data to %s', destination)


if __name__ == '__main__':
    main()
