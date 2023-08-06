"""Fava's options.

Options for Fava can be specified through Custom entries in the Beancount file.
This module contains a list of possible options, the defaults and the code for
parsing the options.

"""

import copy
from collections import namedtuple
import re

OptionError = namedtuple('OptionError', 'source message entry')
InsertEntryOption = namedtuple('InsertEntryOption', 'date re filename lineno')

DEFAULTS = {
    'account-journal-include-children': True,
    'auto-reload': False,
    'default-file': None,
    'editor-print-margin-column': 60,
    'extensions': [],
    'import-config': None,
    'import-dirs': [],
    'insert-entry': [],
    'interval': 'month',
    'journal-show': ['transaction', 'balance', 'note', 'document', 'custom',
                     'budget'],
    'journal-show-document': ['discovered', 'statement'],
    'journal-show-transaction': ['cleared', 'pending'],
    'language': None,
    'show-accounts-with-zero-balance': True,
    'show-accounts-with-zero-transactions': True,
    'show-closed-accounts': False,
    'sidebar-show-queries': 5,
    'unrealized': 'Unrealized',
    'upcoming-events': 7,
    'uptodate-indicator-grey-lookback-days': 60,
    'use-external-editor': False,
}

BOOL_OPTS = [
    'account-journal-include-children',
    'auto-reload',
    'show-accounts-with-zero-balance',
    'show-accounts-with-zero-transactions',
    'show-closed-accounts',
    'use-external-editor',
]

INT_OPTS = [
    'editor-print-margin-column',
    'upcoming-events',
    'uptodate-indicator-grey-lookback-days',
    'sidebar-show-queries',
]

LIST_OPTS = [
    'extensions',
    'import-dirs',
    'journal-show',
    'journal-show-document',
    'journal-show-transaction',
]

STR_OPTS = [
    'import-config',
    'interval',
    'language',
    'unrealized',
]


def parse_options(custom_entries):
    """Parse custom entries for Fava options.

    The format for option entries is the following:

        2016-04-01 custom "fava-option" "[name]" "[value]"

    Args:
        custom_entries: A list of Custom entries.

    Returns:
        A tuple (options, errors) where options is a dictionary of all options
        to values, and errors contains possible parsing errors.

    """

    options = copy.deepcopy(DEFAULTS)
    errors = []

    for entry in custom_entries:
        if entry.type == 'fava-option':
            try:
                key = entry.values[0].value
                assert key in DEFAULTS.keys()

                if key == 'default-file':
                    options[key] = entry.meta['filename']
                if key == 'insert-entry':
                    opt = InsertEntryOption(
                        entry.date,
                        re.compile(entry.values[1].value),
                        entry.meta['filename'],
                        entry.meta['lineno'])
                    options[key].append(opt)
                else:
                    value = entry.values[1].value
                    assert isinstance(value, str)

                if key in STR_OPTS:
                    options[key] = value
                elif key in BOOL_OPTS:
                    options[key] = value.lower() == 'true'
                elif key in INT_OPTS:
                    options[key] = int(value)
                elif key in LIST_OPTS:
                    options[key] = str(value).strip().split(' ')
            except (IndexError, TypeError, AssertionError):
                errors.append(
                    OptionError(entry.meta,
                                'Failed to parse fava-option entry', entry))

    return options, errors
