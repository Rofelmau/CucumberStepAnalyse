from pandas.io.json import json_normalize
import os
import json
import io
from re import sub

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


STEP_PREFIXES = ["CUKE_STEP_(", "GIVEN(", "WHEN(", "THEN("]
REGEX_PREFIX = "REGEX_PARAM"
OBJECT_TYPE_ANNOTATION = "//@OBJECT_TYPE: "


class Step(object):

    def __init__(self, text, file_name, object_type=""):
        self.text = text
        self.object_type = object_type
        self.params = list()
        self.file_name = file_name


class Param(object):

    def __init__(self, param_type, param_name, capture):
        self.capture = capture
        self.param_type = param_type
        self.param_name = param_name


def analyse_step_definitions(self, root_path, file_postfix, searched_data):
    steps = _get_step_list(self, root_path, file_postfix)
    _print_as_json(steps, searched_data)
    _json_to_csv(searched_data)
    return len(steps)


def _get_file_list(self, path='.', extension='', path_delimiter='/', file_list=None):

    if file_list is None:
        file_list = list()
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

    for document in file_list:
        current_file = open(document, "r")
        current_file_name_with_dir = current_file.name.split(root_path)
        annotation_found = False
        for line in current_file:
            if REGEX_PREFIX in line:
                capture = _get_param_capture(steps[len(steps) - 1])
                param_type = line.split('(', 1)[1].split(',')[0]
                param_name = line.split('(', 1)[1].split(', ')[1].split(')')[0]
                steps[len(steps)-1].params.append(Param(param_type, param_name, capture))
            elif OBJECT_TYPE_ANNOTATION in line:
                param = line.split(OBJECT_TYPE_ANNOTATION, 1)[1].split('\n')[0]
                steps.append(Step("", current_file_name_with_dir[1], param))
                annotation_found = True
            else:
                for substring in STEP_PREFIXES:
                    if substring in line:
                        text = line.split('("', 1)[1].split('")')[0]
                        if annotation_found:
                            steps[len(steps) - 1].text = text
                            annotation_found = False
                        else:
                            steps.append(Step(text, current_file_name_with_dir[1]))

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


def remove_data_from_json(parant_data, position, outstring):
    key = parant_data[position][0]
    least_one_following_line = False
    if position < len(parant_data) - 1:
        for k in range(position + 1, len(parant_data)):
            least_one_following_line = least_one_following_line or parant_data[k][1].get()

    if len(parant_data[position]) > 2:
        starting_pattern = '\n' + r'( +)' + '"' + key + '": '
        if not least_one_following_line and position > 0:
            starting_pattern = r'(,?)' + starting_pattern

        sub_elements = '\n' + r'( +)' + '{' + '\n'
        count = len(parant_data[position][2])
        for l in range(0,count):
            sub_elements += r'(.+)' + '\n'
        sub_elements += r'( +)' + '}' + r'(,?)'

        ending_sub_element = r'(\s)?' + r'( *)' + ']' + r'(,?)' + '\n'

        outstring = sub(starting_pattern + '\\[' + r'(' + sub_elements + ')*' + ending_sub_element, '\n', outstring)
    else:
        starting_pattern = '\n' + r'( +)' + '"' + key + '": "'
        if not least_one_following_line and position > 0:
            starting_pattern = r'(,?)' + starting_pattern
        outstring = sub(starting_pattern + r'(.+)' + '\n', '\n', outstring)

    return outstring


def _print_as_json(step_list, searched_data):
    outstring = to_unicode('[ \n')
    for step in step_list:
        str_ = json.dumps(step.__dict__, default=lambda o: o.__dict__,
                          indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
        outstring += to_unicode(str_)
        if step_list.index(step) != len(step_list) - 1:
            outstring += to_unicode(",")
        outstring += to_unicode("\n")
    outstring += to_unicode("]")

    least_one_data_selected = False
    for i in range(len(searched_data)):
        if len(searched_data[i]) <= 2:
            least_one_data_selected = least_one_data_selected or searched_data[i][1].get()
        else:
            for j in range(0, len(searched_data[i][2])):
                least_one_data_selected = least_one_data_selected or searched_data[i][2][j][1].get()

    if least_one_data_selected:
        for i in range(len(searched_data)):
            if len(searched_data[i]) <= 2:
                if not searched_data[i][1].get():
                    outstring = remove_data_from_json(searched_data, i, outstring)
            else:
                least_one_sub_selected = False
                for j in range(0, len(searched_data[i][2])):
                    least_one_sub_selected = least_one_sub_selected or searched_data[i][2][j][1].get()
                if not least_one_sub_selected:
                    searched_data[i][1].set(False)
                    outstring = remove_data_from_json(searched_data, i, outstring)
                else:
                    searched_data[i][1].set(True)
                    for j in range(0, len(searched_data[i][2])):
                        if not searched_data[i][2][j][1].get():
                            outstring = remove_data_from_json(searched_data[i][2], j, outstring)

    with io.open('StepDefinitions.json', 'w', encoding='utf8') as outfile:
        outfile.write(outstring)


def _json_to_csv(searched_data):
    with open('StepDefinitions.json') as data_file:
        data = json.load(data_file)

    if searched_data[2][1].get():
        selected_data = []
        for i in range(len(searched_data)):
            if len(searched_data[i]) <= 2 and searched_data[i][1].get():
                selected_data.append(searched_data[i][0])

        n_data = json_normalize(data, 'params', selected_data)
    else:
        n_data = json_normalize(data)
    n_data.to_csv("StepDefinitions.csv")
