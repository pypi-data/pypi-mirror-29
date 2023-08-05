
HTTP daemon to check postgresql server status for haproxy
=========================================================

This repository implements a permanent HTTP daemon to monitor postgresql database state
and to decide which server in configuration is active master.

Response from tool is used by haproxy to redirect traffic to writable postgres master server, to readonly slave
servers and to detect unavailable postgres servers.

Configuration files
-------------------

Configuration path is ~/.config/pgstatus.conf. Configuration file is required if you want to monitor
a postgres server that is not localhost:5432 as user postgres and not using postgres as database to check.

See example configuration file in examples directory.

See example configuration for haproxy in examples/haproxy.conf.

Running the service
-------------------

There is example systemd service unit available in examples/pgstatus-daemon.service, configured by default
to run as postgres user (so normally no user and password needs to be configured for default postgres).

To install:

    cp examples/pgstatus-daemon.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable pgstatus-daemon
    systemctl start pgstatus-daemon

Credits
=======

The basic idea is based on website

https://severalnines.com/blog/postgresql-load-balancing-using-haproxy-keepalived

Instead of xinetd and shell script, this implements the check as a systemd controlled
permanent daemon.
