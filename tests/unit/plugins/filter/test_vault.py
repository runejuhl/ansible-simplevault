# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import timedelta
from decimal import Decimal

import pytest

from ansible import constants as C
from ansible.errors import AnsibleFilterError, AnsibleFilterTypeError
from ansible_collections.petardo.simplevault.plugins.filter.vault import do_vault, do_unvault

vault_password_file = '/tmp/vault_pass.txt'
with open(vault_password_file, 'wb') as f:
    f.write(b'omglolrofl\n')

setattr(C, 'DEFAULT_VAULT_PASSWORD_FILE', vault_password_file)

# We use the @pytest.mark.parametrize decorator to parametrize the function
# https://docs.pytest.org/en/latest/how-to/parametrize.html
# Simply put, the first element of each tuple will be passed to
# the test_convert_to_supported function as the test_input argument
# and the second element of each tuple will be passed as
# the expected argument.
# In the function's body, we use the assert statement to check
# if the convert_to_supported function given the test_input,
# returns what we expect.
@pytest.mark.parametrize('test_input', [
    ('abc'),
    ('1'),
    ("{'a': 12, 'b':\r 42, 54: 45}\n"),
])

def test_do_vault(test_input):
    assert do_unvault(do_vault(test_input)) == test_input

def test_vault_unsupported_type():
    with pytest.raises(AnsibleFilterTypeError, match=r'Can only vault'):
        do_vault(42)

def test_vault_no_vault_file():
    with pytest.raises(AnsibleFilterError, match=r'invalid vault file'):
        setattr(C, 'DEFAULT_VAULT_PASSWORD_FILE', None)
        do_vault('123')
