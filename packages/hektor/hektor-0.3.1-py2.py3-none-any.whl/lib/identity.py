import json

import lib.generic


class JSONIdentityConverter(lib.generic.Converter):
    """ This serves as an identity if you wish to import a json file
    that you generated earlier with hektor and you now want to run a
    preprocessor on it. """

    accepted_files = ('.json',)

    def convert(self, filepath):
        with open(filepath) as json_input:
            return json.load(json_input)
