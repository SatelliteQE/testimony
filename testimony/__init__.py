# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

"""
DocString manipulation methods to create test reports
"""

import ast
import json
import os
import sys

from decimal import Decimal
from testimony.constants import (
    CLR_ERR, CLR_GOOD, CLR_RESOURCE, DOCSTRING_TAGS, PRINT_AUTO_TC,
    PRINT_DOC_MISSING, PRINT_INVALID_DOC, PRINT_MANUAL_TC, PRINT_NO_DOC,
    PRINT_NO_MINIMUM_DOC, PRINT_NO_MINIMUM_DOC_TC,
    PRINT_PARSE_ERR, PRINT_TC_AFFECTED_BUGS, PRINT_TOTAL_TC, PRINT_REPORT,
    SUMMARY_REPORT, VALIDATE_DOCSTRING_REPORT, BUGS_REPORT, MANUAL_REPORT,
    AUTO_REPORT)

try:
    import termcolor
    has_termcolor = True
except ImportError, e:
    has_termcolor = False

settings = {
    'json': False,
    'nocolor': False,
}


class Result(object):
    """Class that represents a path result"""

    def __init__(self, bugs=0, bugs_list=[], invalid_docstring=0,
                 no_docstring=0, no_minimal_docstring=0, manual_count=0,
                 tc_count=0):
        """
        bugs: number of bugs found
        bugs_list: list of bugs found
        invalid_docstrings: number of testcases with invalid docstrings found
        no_docstring: number of testcases with no docstring
        no_minimal_docstring: number of testcases that don't have at least
            feature, test and assert tags
        manual_count: number of testcases that represents manual testing
        tc_count: total number of testcases found
        """

        self.bugs = bugs
        self.bugs_list = bugs_list
        self.invalid_docstring = invalid_docstring
        self.no_docstring = no_docstring
        self.no_minimal_docstring = no_minimal_docstring
        self.manual_count = manual_count
        self.tc_count = tc_count
        self.paths = []


def main(report, paths, json, nocolor):
    """
    Main function for testimony project

    Expects a valid report type and valid directory paths, hopefully argparse
    is taking care of validation
    """

    settings['json'] = json
    settings['nocolor'] = nocolor
    results = []

    for path in paths:
        result = Result()
        for dirpath, dirnames, filenames in os.walk(path):
            dir_contents = {
                'path': dirpath,
                'files': [],
            }

            for filename in filenames:
                if (filename.startswith('test_') and
                        filename.endswith('.py')):
                    filepath = os.path.join(dirpath, filename)
                    list_strings, result = get_docstrings(
                        report, filepath, result)
                    dir_contents['files'].append({
                        'name': filename,
                        'docstrings': list_strings,
                    })
                    if report == SUMMARY_REPORT:
                        #for printing test summary later
                        result = update_summary(list_strings, result)
            result.paths.append(dir_contents)
        results.append(result)

    if json is True:
        print_json_output(report, results)
    else:
        print_text_ouput(report, results)

    #Send error code back to caller
    if any([r.invalid_docstring != 0 or r.no_docstring != 0 for r in results]):
        sys.exit(-1)


def print_text_ouput(report, results):
    """Prints the report output in text format"""
    for result in results:
        for path in result.paths:
            print colored(
                "\nFetching Test Path %s\n",
                attrs=['bold']) % colored(path['path'], CLR_RESOURCE)
            for f in path['files']:
                #Do not print this text for test summary
                if report != SUMMARY_REPORT:
                    print colored(
                        "Scanning %s...", attrs=['bold']) % f['name']
                if report != SUMMARY_REPORT:
                    print_testcases(report, f['docstrings'], result)
        #Print for test summary
        if report == SUMMARY_REPORT:
            print_summary(result)
        #Print total number of invalid doc strings
        if report == VALIDATE_DOCSTRING_REPORT:
            if result.invalid_docstring == 0:
                col = CLR_GOOD
            else:
                col = CLR_ERR
            print colored(
                PRINT_INVALID_DOC,
                attrs=['bold']) % colored(result.invalid_docstring, col)
            if result.no_docstring == 0:
                col = CLR_GOOD
            else:
                col = CLR_ERR
            print colored(
                PRINT_NO_DOC,
                attrs=['bold']) % colored(result.no_docstring, col)
            if result.no_minimal_docstring == 0:
                col = CLR_GOOD
            else:
                col = CLR_ERR
            print colored(
                PRINT_NO_MINIMUM_DOC_TC,
                attrs=['bold']) % colored(result.no_minimal_docstring, col)
        #Print number of test cases affected by bugs and also the list of bugs
        if report == BUGS_REPORT:
            print colored(
                PRINT_TC_AFFECTED_BUGS, attrs=['bold']) % result.bugs
            if len(result.bugs_list) > 0:
                print colored("\nBug list:", attrs=['bold'])
                for bug in result.bugs_list:
                    print bug


def print_json_output(report, results):
    """Prints the report output in JSON format"""

    if report == PRINT_REPORT:
        output = [result.paths for result in results]
    elif report == SUMMARY_REPORT:
        output = [get_summary_result(result) for result in results]
    elif report == VALIDATE_DOCSTRING_REPORT:
        output = [result.__dict__ for result in results]
    elif report == BUGS_REPORT:
        output = [{'bugs': result.bugs,
                   'bugs_list': result.bugs_list} for result in results]
    elif report == MANUAL_REPORT or report == AUTO_REPORT:
        for result in results:
            for path in result.paths:
                for f in path['files']:
                    docstrings = []
                    for docstring in f['docstrings']:
                        status_tag = False
                        for line in docstring:
                            tag = line.split(' ', 1)[0].lower()
                            if DOCSTRING_TAGS[6] in tag:
                                status_tag = True
                        if ((report == AUTO_REPORT and not status_tag) or
                                (report == MANUAL_REPORT and status_tag)):
                            docstrings.append(docstring)
                    f['docstrings'] = docstrings
        output = [result.paths for result in results]
    else:
        # Will not get here because argparse validation, but just to make sure
        raise Exception('Report %s not available' % report)

    print json.dumps(output)


def get_docstrings(report, path, result):
    """
    Function to read docstrings from test_*** methods for a given file
    """
    return_list = []
    obj = ast.parse(''.join(open(path)))
    #The body field inside obj.body[] contains the docstring
    #So first find the body field of obj.body[] array
    for i in range(0, len(obj.body)):
        parameters = obj.body[i]._fields
        for attr in parameters:
            if attr == 'body':
                break
    #Now iterate the found body[] list from obj.body[] to find the docstrings
    #Remember that this body[] list will have all different items like class
    #docstrings and functions. So first find the items which are functions
    for j in range(0, len(obj.body[i].body)):
        item_list = []
        try:
            obj_param = obj.body[i].body[j]._fields
            for attr in obj_param:
                #Retrieve the func name to check if this is a test_* function
                if attr == 'name':
                    func_name = getattr(obj.body[i].body[j], "name")
                    if func_name.startswith('test_'):
                        #Find the docstring value of this function
                        #Remove the trailing spaces
                        value = obj.body[i].body[j].body[0].value.s.lstrip()
                        #Split the docstring with @
                        doclines = value.split('@',)
                        featurefound = False
                        testfound = False
                        assertfound = False
                        for attr in doclines:
                            #Remove trailing spaces
                            attr = attr.rstrip()
                            #Remove any new line characters
                            attr = attr.rstrip('\n')
                            if attr != '':
                                if report == VALIDATE_DOCSTRING_REPORT:
                                    docstring_tag = attr.split(" ", 1)
                                    #Error out invalid docstring
                                    if not any(
                                            x in docstring_tag[0].lower() for
                                            x in DOCSTRING_TAGS):
                                        item_list.append(
                                            "%s: Invalid DocString: %s"
                                            % (func_name, colored(
                                                attr, CLR_ERR,
                                                attrs=['bold'])))
                                        result.invalid_docstring += 1
                                    if (DOCSTRING_TAGS[0] in
                                            docstring_tag[0].lower()):
                                        featurefound = True
                                    if (DOCSTRING_TAGS[1] in
                                            docstring_tag[0].lower()):
                                        testfound = True
                                    if (DOCSTRING_TAGS[4] in
                                            docstring_tag[0].lower()):
                                        assertfound = True
                                elif report == BUGS_REPORT:
                                    #Find the bug from docstring
                                    docstring_tag = attr.split(" ", 1)
                                    if (DOCSTRING_TAGS[5] in
                                            docstring_tag[0].lower()):
                                        item_list.append(attr)
                                        result.bugs += 1
                                        result.bugs_list.append(
                                            docstring_tag[1])
                                else:
                                    #For printing all test cases
                                    item_list.append(attr)
                        if report == VALIDATE_DOCSTRING_REPORT:
                            if (not featurefound or
                                    not testfound or
                                    not assertfound):
                                item_list.append(
                                    "%s: %s" % (
                                        func_name, PRINT_NO_MINIMUM_DOC))
                                result.no_minimal_docstring += 1
                        if len(item_list) != 0:
                            return_list.append(item_list)
        except AttributeError:
            if report == PRINT_REPORT or report == VALIDATE_DOCSTRING_REPORT:
                item_list.append(
                    "%s: %s" % (
                        func_name, colored(PRINT_DOC_MISSING, CLR_ERR)))
                return_list.append(item_list)
            result.no_docstring += 1
            continue
        except:
            print colored(PRINT_PARSE_ERR, CLR_ERR, attrs=['bold'])
    return return_list, result


def print_testcases(report, list_strings, result):
    """
    Prints all the test cases based on given criteria
    """
    tc = 0
    for docstring in list_strings:
        if report == PRINT_REPORT:
            tc = tc + 1
            print "\nTC %d" % tc

        #verify if this needs to be printed
        manual_print = False
        auto_print = True
        for lineitem in docstring:
            docstring_tag = lineitem.split(" ", 1)
            if report == AUTO_REPORT:
                if DOCSTRING_TAGS[6] in docstring_tag[0].lower():
                    auto_print = False
            if report == MANUAL_REPORT:
                if DOCSTRING_TAGS[6] in docstring_tag[0].lower():
                    manual_print = True
        if report == AUTO_REPORT and auto_print is True:
            print_line_item(docstring)
        if report == MANUAL_REPORT and manual_print is True:
            print_line_item(docstring)
        if report == PRINT_REPORT or report == VALIDATE_DOCSTRING_REPORT:
            print_line_item(docstring)


def update_summary(list_strings, result):
    """
    Updates summary for reporting
    """
    for docstring in list_strings:
        result.tc_count += 1
        for lineitem in docstring:
            lineitem = lineitem.lower()
            if lineitem.startswith(DOCSTRING_TAGS[6]) and 'manual' in lineitem:
                result.manual_count += 1
    return result


def get_summary_result(result):
    manual_percent = float(Decimal(result.manual_count) /
                           Decimal(result.tc_count) * 100)
    auto_count = result.tc_count - result.manual_count
    auto_percent = float(Decimal(int(auto_count)) / Decimal(result.tc_count) *
                         100)
    return {
        'path': result.paths[0]['path'],  # get the root path
        'tc_count': result.tc_count,
        'auto_count': auto_count,
        'auto_percent': auto_percent,
        'manual_count': result.manual_count,
        'manual_percent': manual_percent,
        'no_docstring': result.no_docstring,
    }


def print_summary(result):
    """
    Prints summary for reporting
    """
    summary_result = get_summary_result(result)
    print colored(PRINT_TOTAL_TC, attrs=['bold']) % summary_result['tc_count']
    print (colored(PRINT_AUTO_TC, attrs=['bold']) %
           summary_result['auto_count'] +
           '({0:.0f}%)'.format(summary_result['auto_percent']))
    print (colored(PRINT_MANUAL_TC, attrs=['bold']) %
           summary_result['manual_count'] +
           '({0:.0f}%)'.format(summary_result['manual_percent']))
    print (colored(PRINT_NO_DOC, attrs=['bold']) %
           summary_result['no_docstring'])


def print_line_item(docstring):
    """
    Parses the given docstring list to print out each line item
    """
    for lineitem in docstring:
        print lineitem


def colored(text, color=None, attrs=None):
    """
    Checks if termcolor is installed before calling it
    """
    if has_termcolor and not settings['nocolor']:
        return termcolor.colored(text, color=color, attrs=attrs)
    else:
        return text
