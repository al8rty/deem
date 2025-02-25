Resolving: _ldap._tcp.au-team.irpo
Feb 25 22:26:21 cli.au-team.irpo realmd[6367]:  * Performing LDAP DSE lookup on: 192.168.1.2
Feb 25 22:26:21 cli.au-team.irpo realmd[6367]:  * Successfully discovered: au-team.irpo
Feb 25 22:26:24 cli.au-team.irpo realmd[6367]:  * Unconditionally checking packages
Feb 25 22:26:24 cli.au-team.irpo realmd[6367]:  * Resolving required packages
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * LANG=C /usr/sbin/adcli join --verbose --domain au>
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Using domain name: au-team.irpo
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Calculated computer account name from fqdn: CLI
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Using domain realm: au-team.irpo
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Sending NetLogon ping to domain controller: 192.1>
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Received NetLogon info from: hq-srv.au-team.irpo
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Wrote out krb5.conf snippet to /var/cache/realmd/>
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Authenticated as user: Administrator@AU-TEAM.IRPO
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  * Using GSS-SPNEGO for SASL bind
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  ! Couldn't authenticate to active directory: 800903>
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]: adcli: couldn't connect to au-team.irpo domain: Coul>
Feb 25 22:26:25 cli.au-team.irpo realmd[6367]:  ! Insufficient permissions to join the domain
