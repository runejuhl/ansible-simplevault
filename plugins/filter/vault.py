# Mostly copied from lib/ansible/plugins/filter/encryption.py at revision
# 0937cc486219663b6b6e6a178ef40798217864fa.
#
# Licensed under GNU General Public License v3.0 or later.

# Copyright: (c) 2021, Ansible Project

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from jinja2.runtime import Undefined
from jinja2.exceptions import UndefinedError

from ansible import constants as C
from ansible.errors import AnsibleFilterError, AnsibleFilterTypeError
from ansible.module_utils._text import to_native, to_bytes
from ansible.module_utils.six import string_types, binary_type
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.yaml.objects import AnsibleVaultEncryptedUnicode
from ansible.parsing.vault import is_encrypted, VaultSecret, VaultLib, FileVaultSecret
from ansible.utils.display import Display

display = Display()

def load_secret():
    vault_password_file = getattr(C, 'DEFAULT_VAULT_PASSWORD_FILE')

    if not isinstance(vault_password_file, str):
        raise AnsibleFilterError(f'invalid vault file {vault_password_file}')

    loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files

    fvs = FileVaultSecret(filename=vault_password_file, loader=loader)
    fvs.load()
    secret = fvs.bytes

    if not isinstance(secret, binary_type):
        raise AnsibleFilterTypeError(
            "Loaded secret no binary as expected, instead we got: %s" % type(secret))

    return secret

def do_vault(data, salt=None, vaultid='filter_default', wrap_object=False):
    secret = load_secret()

    if not isinstance(data, (string_types, binary_type, Undefined)):
        raise AnsibleFilterTypeError("Can only vault strings, instead we got: %s" % type(data))

    vault = ''
    vs = VaultSecret(secret)
    vl = VaultLib()
    try:
        vault = vl.encrypt(to_bytes(data), vs, vaultid, salt)
    except UndefinedError:
        raise
    except Exception as e:
        raise AnsibleFilterError("Unable to encrypt: %s" % to_native(e), orig_exc=e)

    if wrap_object:
        vault = AnsibleVaultEncryptedUnicode(vault)
    else:
        vault = to_native(vault)

    return vault


def do_unvault(vault, vaultid='filter_default'):
    secret = load_secret()

    if not isinstance(vault, (string_types, binary_type, AnsibleVaultEncryptedUnicode, Undefined)):
        raise AnsibleFilterTypeError(
            "Vault should be in the form of a string, instead we got: %s" % type(vault))

    data = ''
    vs = VaultSecret(secret)
    vl = VaultLib([(vaultid, vs)])
    if isinstance(vault, AnsibleVaultEncryptedUnicode):
        vault.vault = vl
        data = vault.data
    elif is_encrypted(vault):
        try:
            data = vl.decrypt(vault)
        except UndefinedError:
            raise
        except Exception as e:
            raise AnsibleFilterError("Unable to decrypt: %s" % to_native(e), orig_exc=e)
    else:
        data = vault

    return to_native(data)


class FilterModule(object):
    ''' Ansible vault jinja2 filters '''

    def filters(self):
        filters = {
            'simple_vault': do_vault,
            'simple_unvault': do_unvault,
        }

        return filters
