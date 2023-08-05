[![license](https://img.shields.io/github/license/plus3it/mcafee-agent-formula.svg)](./LICENSE)
[![Travis-CI Build Status](https://travis-ci.org/plus3it/mcafee-agent-formula.svg)](https://travis-ci.org/plus3it/mcafee-agent-formula)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/plus3it/mcafee-agent-formula?branch=master&svg=true)](https://ci.appveyor.com/project/plus3it/mcafee-agent-formula)

# mcafee-agent-formula

This salt formula will install McAfee Agent, for use with a McAfee ePolicy
Orchestrator (ePO) server. The formula supports both Linux and Windows.

On Windows, the formula depends on the Salt Windows Package Manager (`winrepo`),
and a `winrepo` package definition must be present for the McAfee Agent.
Configuring `winrepo` is not handled by this formula.

The formula currently supports no configuration of the McAfee Agent itself; it
is assumed all configuration is handled by the ePO server. However, the formula
does use pillar to define the name of the mcafee package, and the version to
install.

## Available States

-   [mcafee-agent](#mcafee-agent)

### mcafee-agent

Installs the McAfee Agent.

## Windows Configuration

This formula supports configuration via pillar for the name of the winrepo
package and the version of the package to install. All settings must be
located within the `mcafee-agent:lookup` pillar dictionary.

### `mcafee-agent:lookup:package`

The `package` parameter is the name of the package as defined in the winrepo
package definition.

>**Required**: `False`
>
>**Default**: `mcafee-agent`

**Example**:

```yaml
mcafee-agent:
  lookup:
    package: mcafee-agent
```

### `mcafee-agent:lookup:version`

The `version` parameter is the version of the package as defined in the
winrepo package definition.

>**Required**: `False`
>
>**Default**: `''`

**Example**:

```yaml
mcafee-agent:
  lookup:
    version: '4.8.2003'
```

## Linux Configuration

The only _required_ configuration setting for Linux systems is the source URL
to the McAfee Agent installer. There are a few other optional settings
described below, as well. All settings must be located within the
`mcafee-agent:lookup` pillar dictionary.

### `mcafee-agent:lookup:source`

The `source` parameter is the URL to the McAfee Agent installer.

>**Required**: `True`
>
>**Default**: `None`

**Example**:

```yaml
mcafee-agent:
  lookup:
    source: https://S3BUCKET.F.Q.D.N/mcafee/linux/mcafee-agent/dev/install.sh
```

### `mcafee-agent:lookup:source_hash`

The `source_hash` parameter is the URL to hash of the McAfee Agent installer.

>**Required**: `True`
>
>**Default**: `None`

**Example**:

```yaml
mcafee-agent:
  lookup:
    source_hash: https://S3BUCKET.F.Q.D.N/mcafee/linux/mcafee-agent/dev/install.sh.SHA512
```

### `mcafee-agent:lookup:keystore_directory`

The `keystore_directory` parameter is the directory where McAfee SSL keyfiles
are stored on the system.

>**Required**: `False`
>
>**Default**: `/opt/McAfee/cma/scratch/keystore`

**Example**:

```yaml
mcafee-agent:
  lookup:
    keystore_directory: /opt/McAfee/cma/scratch/keystore
```

### `mcafee-agent:lookup:key_files`

The `key_files` parameter is a list of key files to look for, in the
`keystore_directory`. If any of these files are found, the formula assumes the
McAfee Agent is already installed and the install is skipped.

>**Required**: `False`
>
>**Default**: _See example below_

**Example**:

```yaml
mcafee-agent:
  lookup:
    key_files:
      - agentprvkey.bin
      - agentpubkey.bin
      - serverpubkey.bin
      - serverreqseckey.bin
```

### `mcafee-agent:lookup:rpms`

The `rpms` parameter is a list of RPMs to look for. If any of these packages
are already installed, the formula skips the installation of the McAfee Agent.

>**Required**: `False`
>
>**Default**: _See example below_

**Example**:

```yaml
mcafee-agent:
  lookup:
    rpms:
      - MFEcma
      - MFErt
```

### `mcafee-agent:lookup:client_in_ports`

The `client_in_ports` parameter is a list of ports to enable inbound for remote
management of the McAfee Agent.

>**Required**: `False`
>
>**Default**: _See example below_

**Example**:

```yaml
mcafee-agent:
  lookup:
    client_in_ports:
      - 8591
```
