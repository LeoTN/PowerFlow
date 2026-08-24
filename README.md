<div align="center">

[![PowerRules](https://raw.githubusercontent.com/LeoTN/PowerRules/development/assets/logo/readme_logo.svg)](https://github.com/LeoTN/PowerRules)

[![latest-version](https://img.shields.io/github/v/release/LeoTN/PowerRules?&filter=*.*.*&display_name=release&style=for-the-badge&logo=Rocket&logoColor=green&label=LATEST&color=green)](https://github.com/LeoTN/PowerRules/releases/latest)
[![latest-beta-version](https://img.shields.io/github/v/release/LeoTN/PowerRules?&include_prereleases&filter=*.*.*b*&display_name=release&style=for-the-badge&logo=Textpattern&logoColor=orange&label=LATEST%20BETA&color=orange)](https://github.com/LeoTN/PowerRules/releases)
[![license](https://img.shields.io/github/license/LeoTN/PowerRules?&style=for-the-badge&logo=Google%20Docs&logoColor=blue&label=License&color=blue)](https://github.com/LeoTN/PowerRules/blob/main/LICENSE)

</div>

#

* [About](#about)
* [Getting Started](#getting-started)
* [Features](#features)
* [Supported Platforms](#supported-platforms)
* [Credits & License](#credits--license)

## About

PowerRules allows you to define rules that automatically control the power state of your computer based on configurable conditions.

Rules are evaluated from top to bottom. The first matching rule executes its configured action.

## Getting Started

**Install with pip:**

```bash
pip install powerrules
```

**Create a policy file:**

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/LeoTN/PowerRules/development/assets/schema/powerrules_policy.schema.json

rules:
  - name: "Shutdown at night after weekend backup"
    conditions:
      and:
        - process:
            name: "backup.exe"
            running: false
        - datetime:
            between:
              start: "23"
              end: "06"
        - datetime:
            weekday: ["Saturday", "Sunday"]
    action:
      type: shutdown
```

**Validate the policy:**

```bash
pwru policy validate
```

**Show configured rules:**

```bash
pwru policy show
```

**Evaluate the policy once:**

```bash
pwru policy run --once
```

**Run continuously:**

```bash
pwru policy run
```

Use a different policy file with `--policy` or `-p`:

```bash
pwru policy run --policy my-policy.yaml
```

## Features

| Feature | Description |
|---------|-------------|
| **Rule-based power management** | Define ordered rules with conditions and power actions |
| **Process conditions** | Match rules based on whether a process is running |
| **Time conditions** | Match time ranges and weekdays |
| **Logical conditions** | Combine conditions using `and`, `or`, and `not` |
| **Power actions** | Shutdown, sleep, hibernate, and reboot |
| **Continuous evaluation** | Evaluate policies repeatedly |
| **First-match execution** | Only the first matching rule is executed once until another rule matches |

## Supported Platforms

| Platform | Status |
|----------|:------:|
| Windows 10/11 | ✅ |
| Linux | Planned |
| macOS | Planned |

## Credits & License

* [Pydantic](https://github.com/pydantic/pydantic) → configuration validation
* [PyYAML](https://github.com/yaml/pyyaml) → YAML policy parsing
* [Typer](https://github.com/fastapi/typer) → command-line interface
* [psutil](https://github.com/giampaolo/psutil) → process information
* [Inkscape](https://inkscape.org) → program used to design the logo

*This repository is licensed under the [MIT License](https://github.com/LeoTN/PowerRules/blob/main/LICENSE).*
