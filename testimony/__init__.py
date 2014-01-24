# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

"""
DocString manipulation methods to create test reports
"""

import ast
import os

from testimony.constants import DOCSTRING_TAGS, REPORT_TAGS, ANSI_TAGS
from termcolor import colored

try:
    from termcolor import colored
except ImportError, e:
    print "Please install termcolor module."
    sys.exit(-1)


bugs = 0
bug_list = []
invalid_doc_string = 0
manual_count = 0
no_doc_string = 0
tc_count = 0
userinput = None
col_resource = ANSI_TAGS[0]["resource"] 
col_error = ANSI_TAGS[1]["error"]
col_good=ANSI_TAGS[2]["good"]


def main(report, paths):
    """
    Main function for testimony project

    Expects a valid report type and valid directory paths, hopefully argparse
    is taking care of validation
    """
    global bug_list
    global bugs
    global invalid_doc_string
    global userinput

    userinput = report
    for path in paths:
        reset_counts()
        print colored("\nTEST PATH: %s\n", attrs=['bold', 'underline']) % colored(path, col_resource)
        for root, dirs, files in os.walk(path):
            for i in range(1, len(files)):  # Loop for each file
                if str(files[i]).startswith('test_') and str(files[i]).endswith('.py'):  # @IgnorePep8
                    #Do not print this text for test summary
                    if userinput != REPORT_TAGS[1]:
                        print colored("Analyzing %s...", attrs=['bold']) % colored(files[i], col_resource)
                    filepath = os.path.join(os.path.abspath(path), files[i])
                    list_strings = get_docstrings(filepath)
                    if userinput in REPORT_TAGS[0] or userinput in REPORT_TAGS[2:3]:
                        #print the derived test cases
                        print_testcases(list_strings)
                    elif userinput == REPORT_TAGS[4]:
                        #print manual test cases
                        print_testcases(list_strings, test_type="manual")
                    elif userinput == REPORT_TAGS[5]:
                        #print auto test cases
                        print_testcases(list_strings, test_type="auto")
                    else:
                        #for printing test summary later
                        update_summary(list_strings)
        #Print for test summary
        if userinput == REPORT_TAGS[1]:
            print_summary()
        #Print total number of invalid doc strings
        if userinput == REPORT_TAGS[2]:
            if invalid_doc_string == 0:
                col = col_good
            else:
                col = col_error
            print colored("Total Number of invalid docstrings: %s", attrs=['bold']) \
                % colored(invalid_doc_string, col)  # @IgnorePep8
        #Print number of test cases affected by bugs and also the list of bugs
        if userinput == REPORT_TAGS[3]:
            print colored("Total Number of test cases affected by bugs: %d",  attrs=['bold']) % bugs
            print colored("List of bugs:", attrs=['bold'])
            for i in bug_list:
                print "  ", i


def get_docstrings(path):
    """
    Function to read docstrings from test_*** methods for a given file
    """
    global no_doc_string
    global invalid_doc_string
    global bugs
    global bug_list
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
        try:
            obj_param = obj.body[i].body[j]._fields
            for attr in obj_param:
                #Retrieve the func name to check if this is a test_* function
                if attr == 'name':
                    func_name = getattr(obj.body[i].body[j], "name")
                    if func_name.startswith('test'):
                        #Find the docstring value of this function
                        #Remove the trailing spaces
                        value = obj.body[i].body[j].body[0].value.s.lstrip()
                        #Split the docstring with @
                        doclines = value.split('@',)
                        item_list = []
                        for attr in doclines:
                            #Remove trailing spaces
                            attr = attr.rstrip()
                            #Remove any new line characters
                            attr = attr.rstrip('\n')
                            if attr != '':
                                if userinput == REPORT_TAGS[2]:
                                    docstring_tag = attr.split(" ", 1)
                                    #Error out invalid docstring
                                    if not any(x in docstring_tag[0] for x in DOCSTRING_TAGS):  # @IgnorePep8
                                        item_list.append(" Invalid Docstring, '%s'" \
                                            % colored(attr, col_error, attrs=['bold']))  # @IgnorePep8
                                        invalid_doc_string = invalid_doc_string + 1  # @IgnorePep8
                                elif userinput == REPORT_TAGS[3]:
                                    #Find the bug from docstring
                                    docstring_tag = attr.split(" ", 1)
                                    if DOCSTRING_TAGS[5] in docstring_tag[0]:
                                        item_list.append(attr)
                                        bugs = bugs + 1
                                        bug_list.append(docstring_tag[1])
                                else:
                                    #For printing all test cases
                                    item_list.append(attr)
                        if len(item_list) != 0:
                            print colored("%s", col_resource) % func_name
                            return_list.append(item_list)
        except AttributeError:
            if userinput == REPORT_TAGS[0] or userinput == REPORT_TAGS[2]:
                print colored("%s", col_resource) % func_name
                print colored("  Docstring missing. Please update. ", col_error)
            no_doc_string = no_doc_string + 1
            continue
        except:
            print colored("!!!!!Exception in parsing DocString!!!!!", col_error, attrs=['bold'])
    return return_list


def print_testcases(list_strings, test_type=None):
    """
    Prints all the test cases based on given criteria
    """
    global userinput
    tc = 0
    for docstring in list_strings:
        if userinput == REPORT_TAGS[0]:
            tc = tc + 1
            print "TC %d" % tc

        #verify if this needs to be printed
        if test_type is not None:
            manual_print = False
            auto_print = True
            for lineitem in docstring:
                docstring_tag = lineitem.split(" ", 1)
                if test_type == "auto":
                    if DOCSTRING_TAGS[6] in docstring_tag[0]:
                        auto_print = False
                if test_type == "manual":
                    if DOCSTRING_TAGS[6] in docstring_tag[0]:
                        manual_print = True
        if test_type == "auto" and auto_print is True:
            print_line_item(docstring)
        if test_type == "manual" and manual_print is True:
            print_line_item(docstring)
        if userinput == REPORT_TAGS[0] or userinput == REPORT_TAGS[2]:
            print_line_item(docstring)

def update_summary(list_strings):
    """
    Updates summary for reporting
    """
    global tc_count
    global manual_count
    for docstring in list_strings:
        tc_count = tc_count + 1
        for lineitem in docstring:
            if lineitem.startswith("Status") and "Manual" in lineitem:
                manual_count = manual_count + 1


def print_summary():
    """
    Prints summary for reporting
    """
    global tc_count
    global manual_count
    global no_doc_string
    print colored("Total Number of test cases:      %s",  attrs=['bold']) % tc_count
    print colored("Total Number of automated cases: %s",  attrs=['bold']) % (tc_count - manual_count)
    print colored("Total Number of manual cases:    %s",  attrs=['bold']) % manual_count
    print colored("Test cases with no docstrings:   %s",  attrs=['bold']) % colored(no_doc_string, col_error)


def reset_counts():
    """
    Resets all the counts to switch between UI and CLI reports
    """
    global tc_count
    global manual_count
    global no_doc_string
    global invalid_doc_string
    global bugs
    global bug_list
    tc_count = 0
    manual_count = 0
    no_doc_string = 0
    invalid_doc_string = 0
    bugs = 0
    bug_list = []


def print_line_item(docstring):
    """
    Parses the given docstring list to print out each line item
    """
    for lineitem in docstring:
        print lineitem
    print "\n"

def get_root_path():
    """
    Returns correct path to logging config file
    """
    return os.path.realpath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
