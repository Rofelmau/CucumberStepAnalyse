import os
import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str


STEP_PREFIXES = ["CUKE_STEP_(", "GIVEN(", "WHEN(", "THEN("]
REGEX_PREFIX = "REGEX_PARAM"
MAC_TEST_PATH = "/Users/lucaschuller/Documents/GitHub/CocktailCalc"


class Step:

    def __init__(self, text):
        self.text = text
        self.params = list()


def analyse_step_definitions(self, root_path, file_postfix):
    steps = _get_step_list(self, root_path, file_postfix)
    _print_as_json(steps)


def _get_file_list(self, path='.', extension='', path_delimiter='/', file_list=[]):

    for f in os.listdir(path):
        f = path + path_delimiter + f
        if os.path.isdir(f):
            file_list = _get_file_list(self, f, extension, path_delimiter, file_list)
        elif os.path.isfile(f) and f.endswith(extension):
            file_list.append(f)

    return file_list


def _get_step_list(self, root_path, file_postfix):

    steps = list();
    file_list = _get_file_list(self, root_path, file_postfix)
    count = 0;

    for document in file_list:
        count = count+1
        current_file = open(document, "r")

        for line in current_file:
            if REGEX_PREFIX in line:
                param = line.split('(', 1)[1].split(',')[0]
                steps[len(steps)-1].params.append(param)
            else:
                for substring in STEP_PREFIXES:
                    if substring in line:
                        text = line.split('("', 1)[1].split('")')[0]
                        steps.append(Step(text))

    return steps


def _print_as_json(step_list):
    with io.open('StepDefinitions.json', 'w', encoding='utf8') as outfile:
        outfile.write(to_unicode('{\n'))
        outfile.write(to_unicode('  "steps" : [ \n'))
        for step in step_list:
            str_ = json.dumps(step.__dict__, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))
            if step_list.index(step) != len(step_list) - 1:
                outfile.write(to_unicode(","))
            outfile.write(to_unicode("\n"))
        outfile.write(to_unicode("  ]\n}"))
