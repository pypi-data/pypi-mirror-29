from __future__ import absolute_import, division, print_function

import sys
import re
import os
import io

import xml.etree.ElementTree as etree


def parse_nose(text, cwd, param):
    if param is not None:
        raise ValueError("Unknown parameters '{:r}' for parser 'nose'".format(param))

    failures = {}
    test_count = -1

    state = 'initial'
    name = ''
    message = []

    for line in text.splitlines():
        line = line.rstrip()

        m = re.match('^========+$', line)
        if m:
            if state == 'content':
                failures[name] = "\n".join(message)
            state = 'top-header'
            continue

        m = re.match('^(ERROR|FAIL): (.*)$', line)
        if m and state == 'top-header':
            name = m.group(2).strip()
            message = [line]
            state = 'name'
            continue

        m = re.match('^--------+$', line)
        if m and state == 'name':
            state = 'content'
            message.append(line)
            continue
        elif m and state == 'content':
            failures[name] = "\n".join(message)
            state = 'initial'
            continue

        m = re.match('^Ran ([0-9]+) tests? in .*$', line)
        if m and state == 'initial':
            test_count = int(m.group(1))
            continue

        if state == 'content':
            message.append(line)
            continue

    if test_count < 0:
        err_msg = "ERROR: parsing nose output failed"
    else:
        err_msg = None

    warns = _parse_warnings(text, suite="nose")

    return failures, warns, test_count, err_msg


def parse_junit(text, cwd, param):
    if param is not None:
        logfile = param
    else:
        logfile = 'junit.xml'

    xml_fn = os.path.join(cwd, logfile)

    if not os.path.isfile(xml_fn):
        return {}, {}, -1, "ERROR: log file '{}' not found".format(logfile)

    failures = {}
    warns = {}

    try:
        tree = etree.parse(xml_fn)
    except Exception as exc:
        return {}, {}, -1, "ERROR: opening 'junit.xml' failed: {0}".format(exc)

    suite = tree.getroot()
    cases = suite.findall('testcase')

    test_count = len(cases)

    for case in cases:
        failure = case.find('failure')
        if failure is None:
            failure = case.find('error')

        stdout = case.find('system-out')
        stderr = case.find('system-err')
        name = case.attrib['classname'] + '.' + case.attrib['name']

        if stdout is not None:
            stdout = stdout.text
        else:
            stdout = ''

        if stderr is not None:
            stderr = stderr.text
        else:
            stderr = ''

        if (failure is not None and
                failure.attrib.get('type', '') != 'numpy.testing.utils.KnownFailureException'):
            message = "\n".join(["-"*79, name] + failure.text.splitlines())
            failures[name] = message

        # Warnings
        text = stdout + "\n" + stderr
        warns.update(_parse_warnings(text, 'single', name))

    return failures, warns, test_count, None


def _parse_warnings(text, suite, default_test_name=None):
    test_name = ''
    key = None
    w = {}

    for line in text.splitlines():
        line = line.rstrip()

        if suite == 'nose':
            m = re.search(r'^(.*)\s+\.\.\.\s+', line)
            if m:
                key = None
                test_name = m.group(1).strip()
        elif suite == 'pytest':
            m = re.search('^([^\t ]+::test_[^\t ]+)\s+', line)
            if m:
                key = None
                test_name = m.group(1).strip()
        elif suite == 'single':
            test_name = default_test_name
        else:
            raise ValueError()

        m = re.search(r'(/.+\.py):(\d+): (.*Warning: .*)$', line)
        if m:
            key = "{0}\n    {1}:{2}".format(m.group(3),
                                            m.group(1),
                                            m.group(2))
            w.setdefault(key, set()).add(test_name)
            continue

        if key is not None and line.startswith('  '):
            items = w[key]
            del w[key]
            key += "\n" + line.rstrip()
            w[key] = items.union(w.get(key, set()))
        else:
            key = None

    for key in list(w.keys()):
        w[key] = "WARNING: {0}\n{1}\n---".format(key, "\n".join(sorted(w[key])))

    return w


def get_parser(name):
    parsers = {'nose': parse_nose,
               'junit': parse_junit}

    if ':' in name:
        name, param = name.split(':', 1)
    else:
        param = None

    try:
        func = parsers[name]
    except KeyError:
        raise ValueError("Unknown parser name: {0}; not one of {1}".format(name,
                                                                           sorted(parsers.keys())))

    return lambda text, suite: func(text, suite, param)
