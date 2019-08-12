import os
import json
import io
import sys

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


STEP_PREFIXES = ["CUKE_STEP_(", "GIVEN(", "WHEN(", "THEN("]
REGEX_PREFIX = "REGEX_PARAM"
OBJECT_TYPE_ANNOTATION = "//@OBJECT_TYPE: "
MAC_TEST_PATH = "/Users/lucaschuller/Documents/GitHub/CocktailCalc"


class Step(object):

    def __init__(self, text, object_type=""):
        self.text = text
        self.object_type = object_type
        self.params = list()


class Param(object):

    def __init__(self, param, capture):
        self.param = param
        self.capture = capture


def analyse_step_definitions(self, root_path, file_postfix):
    steps = _get_step_list(self, root_path, file_postfix)
    _print_as_json(steps)
    _json_to_pdf()


def _get_file_list(self, path='.', extension='', path_delimiter='/', file_list=[]):

    for f in os.listdir(path):
        f = path + path_delimiter + f
        if os.path.isdir(f):
            file_list = _get_file_list(self, f, extension, path_delimiter, file_list)
        elif os.path.isfile(f) and f.endswith(extension):
            file_list.append(f)

    return file_list


def _get_step_list(self, root_path, file_postfix):

    steps = list()
    file_list = _get_file_list(self, root_path, file_postfix)
    count = 0

    for document in file_list:
        count = count+1
        current_file = open(document, "r")

        annotation_found = False
        for line in current_file:
            if REGEX_PREFIX in line:
                param = line.split('(', 1)[1].split(',')[0]
                capture = _get_param_capture(steps[len(steps)-1])
                steps[len(steps)-1].params.append(Param(param, capture))
            elif OBJECT_TYPE_ANNOTATION in line:
                param = line.split(OBJECT_TYPE_ANNOTATION, 1)[1]
                steps.append(Step("", param))
                annotation_found = True
            else:
                for substring in STEP_PREFIXES:
                    if substring in line:
                        text = line.split('("', 1)[1].split('")')[0]
                        if annotation_found:
                            steps[len(steps) - 1].text = text
                            annotation_found = False
                        else:
                            steps.append(Step(text))

    return steps


def _get_param_capture(step):
    count_params = len(step.params)+1
    splitted_step = step.text.split('(')
    found_noncapture = 0
    for i, _string in enumerate(splitted_step):
        if _string.startswith("?:") and i <= count_params:
            found_noncapture += 1

    capture = splitted_step[count_params+found_noncapture].split(')')[0]
    return capture


def _print_as_json(step_list):
    with io.open('StepDefinitions.json', 'w', encoding='utf8') as outfile:
        outfile.write(to_unicode('{\n'))
        outfile.write(to_unicode('  "steps" : [ \n'))
        for step in step_list:
            str_ = json.dumps(step.__dict__, default=lambda o: o.__dict__,
                              indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)

            outfile.write(to_unicode(str_))
            if step_list.index(step) != len(step_list) - 1:
                outfile.write(to_unicode(","))
            outfile.write(to_unicode("\n"))
        outfile.write(to_unicode("  ]\n}"))


def error_exit(message):
    sys.stderr.write(message)
    sys.exit(1)


def _json_to_pdf():
    fil = open('StepDefinitions.json')
    lis = fil.readlines()
    json_data = json.dumps(lis)
    _print_json_as_pdf(json_data)


def _print_json_as_pdf(json):
    import json
    import csv

    with open('StepDefinitions.json') as f:
        data = json.load(f)

    employee_parsed = json.loads('StepDefinitions.json')
    emp_data = data['steps'][1]['params']
    employ_data = open('TestData.csv', 'w')

    csvwriter = csv.writer(employ_data)

    count = 0
    for emp in emp_data:
        if count == 0:
            header = emp.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(emp.values())
    employ_data.close()
