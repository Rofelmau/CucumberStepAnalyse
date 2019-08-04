import os

STEP_PREFIXES = ["CUKE_STEP_(", "GIVEN(", "WHEN(", "THEN("]
REGEX_PREFIX = "REGEX_PARAM"
MAC_TEST_PATH = "/Users/lucaschuller/Documents/GitHub/CocktailCalc"

class Step:

    def __init__(self, text):
        self.text = text
        self.params = list()


def analyse_step_definitions(self, root_path, file_postfix):
    _get_step_list(self, MAC_TEST_PATH, file_postfix)


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

    # print(count)
    # print(steps[0].text)
    # print(len(steps[0].params))
    # print(steps[0].params[0])
    # print(steps[0].params[1])
    # print(steps[1].text)
    # print(len(steps[1].params))
    # print(steps[1].params[0])
