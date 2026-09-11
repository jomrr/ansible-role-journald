# Ansible Role: journald

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-journald)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-journald)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-journald)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-journald/dev.yml?branch=dev&event=push&label=dev)](https://github.com/jomrr/ansible-role-journald/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-journald/main.yml?branch=main&event=push&label=main)](https://github.com/jomrr/ansible-role-journald/actions/workflows/main.yml?query=branch%3Amain)

Ansible role to configure systemd-journald.

## Purpose

Configure the default systemd journal instance and keep it running. Manage
storage, retention, compression, message priorities and local forwarding.
The default configuration uses persistent storage when /var/log is writable.

## Scope

### Managed

- The main /etc/systemd/journald.conf configuration file.
- The enabled and started state of systemd-journald.service.
- A service restart followed by the journal flush service when configuration
  changes.

### Not Managed

- Installation or replacement of the operating system's init system.
- Journal namespaces, journald.conf.d drop-ins and per-service logging
  overrides.
- Remote log collectors, sealing keys and removal of existing journal data.

## Requirements

- A supported Linux host booted with systemd and systemd-journald installed.
- A writable /var/log filesystem for persistent storage.

## Dependencies

```yaml
collections:
  - name: community.general
    version: '>=12.0.0'
```

## Role Variables

### `journald_storage`

Type: `str`. Required: `false`.

Storage mode for journal data.

Default:

```yaml
journald_storage: persistent
```

### `journald_compress`

Type: `str`. Required: `false`.

Journal compression switch or compression threshold in bytes.

Default:

```yaml
journald_compress: 'yes'
```

### `journald_seal`

Type: `str`. Required: `false`.

Enable forward secure sealing when sealing keys are available.

Default:

```yaml
journald_seal: 'yes'
```

### `journald_split_mode`

Type: `str`. Required: `false`.

Split persistent journals by user; login is a legacy systemd value.

Default:

```yaml
journald_split_mode: uid
```

### `journald_sync_interval_sec`

Type: `str`. Required: `false`.

Maximum interval between journal synchronization operations.

Default:

```yaml
journald_sync_interval_sec: 5m
```

### `journald_rate_limit_interval_sec`

Type: `str`. Required: `false`.

Per-service rate limiting interval; zero disables rate limiting.

Default:

```yaml
journald_rate_limit_interval_sec: 30s
```

### `journald_rate_limit_burst`

Type: `str`. Required: `false`.

Per-service message burst before the filesystem-dependent multiplier.

Default:

```yaml
journald_rate_limit_burst: '1000'
```

### `journald_system_max_use`

Type: `str`. Required: `false`.

Maximum persistent journal size; an empty string uses the systemd default.

Default:

```yaml
journald_system_max_use: 4G
```

### `journald_system_keep_free`

Type: `str`. Required: `false`.

Space to leave free on the persistent journal filesystem; empty uses the systemd
default.

Default:

```yaml
journald_system_keep_free: 1G
```

### `journald_system_max_file_size`

Type: `str`. Required: `false`.

Maximum persistent journal file size; empty uses the systemd default.

Default:

```yaml
journald_system_max_file_size: 128M
```

### `journald_system_max_files`

Type: `str`. Required: `false`.

Maximum persistent journal file count; empty uses the systemd default.

Default:

```yaml
journald_system_max_files: '100'
```

### `journald_runtime_max_use`

Type: `str`. Required: `false`.

Maximum volatile journal size; empty uses the systemd default.

Default:

```yaml
journald_runtime_max_use: 256M
```

### `journald_runtime_keep_free`

Type: `str`. Required: `false`.

Space to leave free on the runtime filesystem; empty uses the systemd default.

Default:

```yaml
journald_runtime_keep_free: 128M
```

### `journald_runtime_max_file_size`

Type: `str`. Required: `false`.

Maximum volatile journal file size; empty uses the systemd default.

Default:

```yaml
journald_runtime_max_file_size: 32M
```

### `journald_runtime_max_files`

Type: `str`. Required: `false`.

Maximum volatile journal file count; empty uses the systemd default.

Default:

```yaml
journald_runtime_max_files: '10'
```

### `journald_max_retention_sec`

Type: `str`. Required: `false`.

Maximum journal retention time; empty leaves the systemd default without a time
limit.

Default:

```yaml
journald_max_retention_sec: ''
```

### `journald_max_file_sec`

Type: `str`. Required: `false`.

Maximum time before journal file rotation; empty uses the systemd default.

Default:

```yaml
journald_max_file_sec: 1month
```

### `journald_forward_to_syslog`

Type: `str`. Required: `false`.

Forward journal messages to the local syslog socket.

Default:

```yaml
journald_forward_to_syslog: 'no'
```

### `journald_forward_to_kmsg`

Type: `str`. Required: `false`.

Forward journal messages to the kernel log buffer.

Default:

```yaml
journald_forward_to_kmsg: 'no'
```

### `journald_forward_to_console`

Type: `str`. Required: `false`.

Forward journal messages to the configured console.

Default:

```yaml
journald_forward_to_console: 'no'
```

### `journald_forward_to_wall`

Type: `str`. Required: `false`.

Forward journal messages to logged-in users according to the wall priority
limit.

Default:

```yaml
journald_forward_to_wall: 'yes'
```

### `journald_tty_path`

Type: `str`. Required: `false`.

Console device for forwarded messages; empty uses the systemd default.

Default:

```yaml
journald_tty_path: /dev/console
```

### `journald_max_level_store`

Type: `str`. Required: `false`.

Least severe priority retained in journal storage.

Default:

```yaml
journald_max_level_store: debug
```

### `journald_max_level_syslog`

Type: `str`. Required: `false`.

Least severe priority forwarded to the syslog socket.

Default:

```yaml
journald_max_level_syslog: debug
```

### `journald_max_level_kmsg`

Type: `str`. Required: `false`.

Least severe priority forwarded to the kernel log buffer.

Default:

```yaml
journald_max_level_kmsg: notice
```

### `journald_max_level_console`

Type: `str`. Required: `false`.

Least severe priority forwarded to the console.

Default:

```yaml
journald_max_level_console: info
```

### `journald_max_level_wall`

Type: `str`. Required: `false`.

Least severe priority forwarded to logged-in users.

Default:

```yaml
journald_max_level_wall: emerg
```

### `journald_line_max`

Type: `str`. Required: `false`.

Maximum stream log line size; empty uses the systemd default.

Default:

```yaml
journald_line_max: 48K
```

### `journald_read_kmsg`

Type: `str`. Required: `false`.

Read messages from the kernel log buffer when accessible.

Default:

```yaml
journald_read_kmsg: 'yes'
```

### `journald_audit`

Type: `str`. Required: `false`.

Request kernel auditing when the journal service has the required capability.

Default:

```yaml
journald_audit: 'yes'
```

## Managed Files

- `/etc/systemd/journald.conf` Owned by root with mode 0644; replaced
  configurations are backed up.

## Check Mode

Configuration and service tasks predict changes without applying them in check
mode.

## Service Behavior

Configuration changes restart journald and then run
systemd-journal-flush.service
at the normal Ansible handler boundary. Flushing activates persistent storage
when allowed by the configured storage mode, including after a change from
volatile.

### Handlers

- JOURNALD | Restart the journal service
- JOURNALD | Apply the configured persistent storage mode

## Security Notes

- Forwarding to syslog, the kernel log buffer and the console is disabled by
  default.
- Forward secure sealing requires existing sealing keys; the role does not
  create keys.

## Operational Notes

- Storage defaults provide a starting point for a VM with 8 GB RAM and an 8 GB
  log volume. Persistent journal usage is limited to 4G with 1G of free-space
  headroom and a maximum journal file size of 128M.
- RuntimeMaxUse limits volatile journal usage to 256M, RuntimeKeepFree leaves
  128M of free-space headroom on the filesystem containing /run/log/journal, and
  RuntimeMaxFileSize limits individual files to 32M. The reserve does not
  allocate memory. Adjust these values to the actual /run filesystem capacity
  and logging workload; no fixed reserve guarantees free space against writes by
  other processes.
- Size settings accept bytes or binary K, M, G, T, P and E suffixes, not
  percentages. Optional limits accept an empty string to omit the directive and
  use systemd's default. Boolean settings retain the string interface, for
  example "yes" and "no"; priorities accept systemd priority names or numbers.
- Existing drop-ins take precedence over the main configuration. Their settings
  must be coordinated with this role. Per-service settings can also override
  journal defaults.
- Journald has no standalone native validator for a candidate journald.conf.
  Argument specifications validate the public interface; Molecule exercises log
  ingestion, persistent and volatile storage, priority filtering, configuration
  changes and check mode. Journal file verification and systemd unit
  verification do not validate journald.conf.
- Journald uses volatile storage during early boot until
  systemd-journal-flush.service requests persistent storage. Switching to
  volatile storage leaves existing persistent journal files intact.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
| --------- | ------------ | ------- | --------------- |
| RedHat | AlmaLinux | latest | [jomrr/molecule-almalinux:latest](https://hub.docker.com/r/jomrr/molecule-almalinux) |
| Archlinux | Archlinux | latest | [jomrr/molecule-archlinux:latest](https://hub.docker.com/r/jomrr/molecule-archlinux) |
| Debian | Debian | latest | [jomrr/molecule-debian:latest](https://hub.docker.com/r/jomrr/molecule-debian) |
| RedHat | Fedora | latest | [jomrr/molecule-fedora:latest](https://hub.docker.com/r/jomrr/molecule-fedora) |
| Suse | OpenSuse Leap | latest | [jomrr/molecule-opensuse-leap:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-leap) |
| Debian | Ubuntu | latest | [jomrr/molecule-ubuntu:latest](https://hub.docker.com/r/jomrr/molecule-ubuntu) |

## Example Playbook

### Configure persistent logging

Keep the default runtime reserve and limit persistent journal usage.

```yaml
---
- name: Configure system logging
  hosts: all
  gather_facts: true
  roles:
    - role: jomrr.journald
      journald_system_max_use: "2G"
      journald_runtime_keep_free: "128M"
```

### Configure volatile logging on a small runtime filesystem

Adjust both the usage limit and free-space reserve to the host's capacity.

```yaml
---
- name: Configure volatile logging
  hosts: all
  gather_facts: true
  roles:
    - role: jomrr.journald
      journald_storage: "volatile"
      journald_runtime_max_use: "128M"
      journald_runtime_keep_free: "64M"
      journald_runtime_max_file_size: "16M"
```

## References

- [journald.conf documentation](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html)
- [systemd journal service](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html)

## Author

[Jonas Mauer](https://github.com/jomrr)

## License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for the full license text.

Copyright (c) 2024 Jonas Mauer.
