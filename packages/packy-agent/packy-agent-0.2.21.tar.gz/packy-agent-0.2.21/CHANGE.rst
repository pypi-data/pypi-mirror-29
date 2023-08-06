Version 0.2.21
--------------
* FIX: Packy Server is requested with timeout
* UPGRADE: Upgraded to requests==2.18.4, idna==2.6, urllib3==1.22

Version 0.2.20
--------------
* UPGRADE: Upgraded Celery to 4.1.0

Version 0.2.19
--------------
* FIX: Clean up for traceroute results submission

Version 0.2.18
--------------
* FEATURE: Support for "Simplified agent deployment"

Version 0.2.17
--------------
* IMPROVEMENT: Restrict highest upgradable version from server
* IMPROVEMENT: Use API v2 to get agent configuration

Version 0.2.16
--------------
* FIX: Fix for getting uptime inside docker container
* CHANGE: Libraries upgrade: `amqp==2.2.2`, `billiard==3.5.0.3`, `kombu==4.1.0`,
  `speedtest-cli==1.0.7`, `supervisor==3.3.3`

Version 0.2.15
--------------
* FEATURE: Agent data usage monitoring
* CHANGE: API v2 is used for measurements submission

Version 0.2.14
--------------
* IMPROVEMENT: New options for `python -m packy_agent.cli.configure`: `--control-server-port 80`,
  `--remove-nginx-default-landing`
* FIX: Bug fixes

Version 0.2.13
--------------
* IMPROVEMENT: Log rotation for Packy Agent, Control Server and Watchdog
* IMPROVEMENT: Better handling log directories creation with Armbian's log2ram service
* CHANGE: Task chaining removed for Ping, Trace and Speedtest modules

Version 0.2.12
--------------
* FEATURE: HTTP module
* FEATURE: Update configuration file from server on agent start
* FIX: Bug fixes

Version 0.2.11
--------------
* FIX: Speedtest bug work-around

Version 0.2.10
--------------
* FEATURE: Command line activation via `packy-agent-activate` tool
* FEATURE: `install` task with explicit version (to be used for downgrades and testing)
* IMPROVEMENT: Agent activation is done in a single HTTP request (this should improve activate
  success on poor networks and also reduce number of orphan agents)
* IMPROVEMENT: `upgrade`/`upgrade_self` task upgrades not only Python Package, but also upgrades
  and configures infrastructure components like supervisord, uWSGI and nginx
* CHANGE: `update_self` renamed to `upgrade`

Version 0.2.9
-------------
* IMPROVEMENT: Most of the installation script is moved into Packy Agent and written in Python
* IMPROVEMENT: `null` is sent instead of '* * *' for unknown hop
* FIX: Installation script fix for upgrade: `service packy start/stop` fix (added systemd support)
* FIX: Watchdog loop wait bug fix

Version 0.2.8
-------------
* IMPROVEMENT: Support of network configuration for Armbian along with better OS flavor detection
* FEATURE: Orange Pi Zero setup instruction
* FIX: Fix for "Reset Activation" feature

Version 0.2.7
-------------
* IMPROVEMENT: uWSGI is put behind nginx

Version 0.2.6.1
---------------
* FIX: Agent activation bug fix

Version 0.2.6
-------------
* FEATURE: Watchdog
* FEATURE: Logout for Control Server
* FIX: Time for measurements is sent in UTC

Version 0.2.5
-------------
* FEATURE: Control Server authentication
* FEATURE: Support for `version`, `ip_address` and `public_ip_address` update for agents
           on heartbeat
* FEATURE: Restart task

Version 0.2.4
-------------
* FEATURE: New in Control Server:

    - Beagel style UI (the same of for Packy Server) with usability improvements
    - Agent status page
    - Network configuration
    - Agent running state control: start/stop/restart agent (as supervisor program), reboot
    - Version upgrade
    - Reset to default settings: agent activation and network configuration
    - Debug information (in debug mode): logs tail and configuration files

* FEATURE: Support for installation directly onto operating system: creation of directories,
  generation of supervisor configuration file and init.d script
* FEATURE: Support for token expiration (required because we no longer generate a new token on each
  task run)
* FEATURE: Support for running Configuration Server and Packy Agent with supervisord in development
  environment
* IMPROVEMENT: Running Control Server with uWSGI
* IMPROVEMENT: Celery (Packy Agent) exists with appropriate message if Agent has not been activated
* IMPROVEMENT: Improved error reporting on agent activation failure
* IMPROVEMENT/FIX: Bootstrap server does not ask for activation if agent has already been activated
* IMPROVEMENT/FIX: Refactoring of configuration file management: avoid rereading up to date file,
  atomic file writes, decoupled configuration of boostrap server, agent, flask, celery,
  reads/writes to configuration files are encapsulated in classes
* FIX: New token is no longer generates a new token on each task run (this were polluting
  Packy Server database with waste token records)
* FIX: Small changes: using floats instead of decimals for measurements

Version 0.2.3
-------------
* Improved `README.rst` for running Packy Agent in development mode with root privileges
* Packy Server compatibility changes

Version 0.2.2
-------------
* Reliable online status support
* Compatibility with Packy Server v0.0.8 and later

Version 0.2.1
-------------
* Traceroute is fixed and refactored: performance increase (15-20 seconds per task), bug fix
* Speedtest task is fixed with improvements: `speedtest-cli` is installed as dependency and
  access via Python API instead of running a subprocess, bug fixes
* Improved logging for Bootstrap Server

Version 0.2.0
-------------
* Dockerization (got rid of in-house tar packaging)
* update_self works via private PyPI (got rid of rsync)
* Bootstrap Server (Flask implementation) with improved error reporting
* Configuration files refactoring

Version 0.0.1
-------------
* Python packaging
* Configurable tasks name prefix
* Configuration files refactoring and introduction of YAML-configuration files
* Created `PackyServerClient`
* `python -m packy_agent.cli.register_agent` command (refactored from `generate_key`)
* New `python -m packy_agent.cli.get_bundle_config` command
