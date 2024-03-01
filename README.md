# Ansible Collection - petardo.simplevault

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
                    | simple_vault(wrap_object=true)
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
        | simple_vault(wrap_object=true)
        | simple_unvault
      }}
  delegate_to: 'localhost'
```
