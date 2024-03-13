# Ansible Collection - runejuhl.simplevault

An Ansible filter plugin to `vault` and `unvault` using
`DEFAULT_VAULT_PASSWORD_FILE` (e.g. set using `vault_password_file` in the
`defaults` section in `ansible.cfg`).

## Usage

``` yaml
- name: 'Read shadow file'
  ansible.builtin.slurp:
    src: '/etc/shadow
  register: 'shadow'

- name: 'Write vaulted shadow to local file'
  ansible.builtin.copy:
    content: |
      {{
        {
          'shadow': shadow.content
                    | b64decode
                    | runejuhl.simplevault.vault(wrap_object=true)
        } | to_nice_yaml
      }}
    dest: '/tmp/vaulted_shadow.yml'
  delegate_to: 'localhost'
```

```yaml
- name: 'vault and unvault'
  ansible.builtin.debug:
    msg: |-
      {{
        'omg'
        | runejuhl.simplevault.vault(wrap_object=true)
        | runejuhl.simplevault.unvault
      }}
  delegate_to: 'localhost'
```
