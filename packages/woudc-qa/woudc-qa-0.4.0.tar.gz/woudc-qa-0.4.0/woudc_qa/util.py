# =================================================================
#
# Terms and Conditions of Use
#
# Unless otherwise noted, computer program source code of this
# distribution is covered under Crown Copyright, Government of
# Canada, and is distributed under the MIT License.
#
# The Canada wordmark and related graphics associated with this
# distribution are protected under trademark law and copyright law.
# No permission is granted to use them outside the parameters of
# the Government of Canada's corporate identity program. For
# more information, see
# http://www.tbs-sct.gc.ca/fip-pcim/index-eng.asp
#
# Copyright title to all 3rd party software distributed with this
# software is held by the respective copyright holders as noted in
# those files. Users are asked to read the 3rd Party Licenses
# referenced with those assets.
#
# Copyright (c) 2016 Government of Canada
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

# Common utility functions

import logging
import csv
from StringIO import StringIO

LOGGER = logging.getLogger(__name__)


def get_extcsv_value(extcsv, table, field, table_index=1, raw=False,
                     payload=False):
    """
    get value or values from extcsv

    :param extcsv: woudc_extcsv.Reader object
    :param table: table to retrieve data from
    :param table_index: index of table
    :param field: field to retrieve data from
    :param payload: profile or non-profile
    :param raw: return raw form
    :returns: value or list of values
    """

    if table_index > 1:
        table = '%s%s' % (table, table_index)

    if payload is False:
        value = None
        if table in extcsv.sections.keys():
            if field in extcsv.sections[table].keys():
                try:
                    value = extcsv.sections[table][field]
                    return value
                except Exception as err:
                    msg = 'Unable to get value for table: %s, field: %s. \
                        Due to: %s.' % (table, field, str(err))
                    LOGGER.error(msg)
                    raise err(msg)
        return value
    if payload:
        value = None
        if table in extcsv.sections.keys():
            body = StringIO(extcsv.sections[table]['_raw'])
            if raw:
                return body
            data_rows = csv.reader(body)
            fields = data_rows.next()
            value = []
            for row in data_rows:
                if field in fields:
                    try:
                        value.append(row[fields.index(field)])
                    except IndexError as err:
                        msg = 'Empty column for table: %s, field: %s.\
                        Putting in blank' % (table, field)
                        value.append('')
                    except Exception as err:
                        msg = 'Unable to get value for table: %s, field: %s.\
                        Due to: %s' % (table, field, str(err))
                        LOGGER.error(msg)
                        raise err(msg)
        return value


def set_extcsv_value(extcsv, table, field, value, table_index=1,
                     mode='update'):
    """
    update extcsv with given value(s)

    :param extcsv: woudc_extcsv.Reader object to be updated
    :param table: table to be updated
    :param table_index: index of table to be updated
    :param field: field to be updated
    :param value: singe value or a list of values (profile)
    :returns: updated extcsv
    """

    if table_index > 1:
        table = '%s%s' % (table, table_index)

    if not isinstance(value, list):  # not a list/profile
        if mode == 'add':
            extcsv.sections[table] = {field: str(value)}
        else:
            extcsv.sections[table][field] = str(value)
    else:  # profile
        # update profile with new values
        try:
            body = get_extcsv_value(extcsv, table, field, table_index, True,
                                    True)
        except Exception as err:
            msg = 'Unable to get value for table: %s, ' \
                  'table_index: %s, field: %s. Due to: %s' % (table,
                                                              table_index,
                                                              field, str(err))
            LOGGER.error(msg)
            raise err(msg)

        new_rows = []
        rows = csv.reader(body)
        fields = rows.next()
        if mode == 'add':
            fields.append(field)
            row_count = 0
            for row in rows:
                try:
                    row.append(value[row_count])
                except IndexError:
                    row.append(None)
                    pass
                new_rows.append(row)
                row_count += 1
        else:
            field_index = fields.index(field)
            row_count = 0
            for row in rows:
                row[field_index] = value[row_count]
                new_rows.append(row)
                row_count += 1

        # write updated profile
        new_payload = StringIO()
        csv_writer = csv.writer(new_payload)
        csv_writer.writerow(fields)
        for row in new_rows:
            try:
                csv_writer.writerow(row)
            except Exception as err:
                msg = 'Unable to write row to payload. Due to: %s' % (str(err))
                LOGGER.error(msg)
                continue
        value = new_payload.getvalue()
        new_payload.close()
        set_extcsv_value(extcsv, table, '_raw', value)

    return extcsv


def summarize(qa_result):
    """
    summarize qa result

    :param qa_result: raw qa result
    :returns: list of summary strings of the form
    """

    # iterate over test results by row:
    v_id = 0
    violations = []
    test_def = None
    fail = '0'
    error_type = 'error'
    for file, tests in qa_result.iteritems():
        for test_id, rows in tests.iteritems():
            test_id = test_id
            if 'P' not in test_id:  # skip pre-condition test results
                test_def = rows['test_def']
                for k, v in rows.iteritems():
                    if k != 'test_def':
                        row_num = k
                        result = v['result']
                        if result == fail:  # summary all failed qa
                            ss = _build_summary_string(
                                v_id,
                                error_type,
                                test_id,
                                row_num,
                                test_def)
                            if ss is not None:
                                violations.append(ss)
                                v_id += 1

    return violations


def _build_summary_string(
        violation_id,
        error_type,
        test_id,
        row_number,
        test_def):
    """
    build qa result summary message like so:
    [violation-id]-[error-type]-[test-id]-[table]\
    -[table index]-[field]-[row number]-[message]

    :returns: summary string
    """
    function = test_def['function']
    msg_stem = 'WOUDC data quality assessment failed.'
    messages = {
        'RC_1': '%s Due to value = x outside the range:\
a <= x <= b, where a=A, b=B' % msg_stem,
        'RC_5': '%s Due to value is less then A' % msg_stem,
        'RC_6': '%s Due to value is greater then A' % msg_stem,
    }

    if function in messages.keys():
        msg = messages[function]

        msg = msg.replace('A', test_def['function_parameter_a'])
        if function == 'RC_1':
            msg = msg.replace('B', test_def['function_parameter_b'])
    else:
        # msg = msg_stem
        return None

    table = test_def['table']
    table_ix = test_def['table_index']
    field = test_def['element']

    summary = '%s-%s-%s-%s-%s-%s-%s-%s' % (
        violation_id,
        error_type,
        test_id,
        table,
        table_ix,
        field,
        row_number,
        msg)

    return summary


def get_table_count(extcsv, table):
    """
    Return the number of occurance of tables in
    extcsv
    """
    count = 0
    for t in extcsv.sections.keys():
        if table in t:
            count += 1

    return count


def get_table_ranges(extcsv, table, table_index):
    """
    Determine range of tables to assess based on
    input table_index
    """
    a = None
    b = None
    if table_index == 'all':
        a = 1
        b = get_table_count(extcsv, table) + 1
    else:
        a = table_index
        b = table_index + 1

    return [a, b]
