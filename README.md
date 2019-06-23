# bwg-api
wbg Api

## help

```
-> python -m bwg.bwg_api -h
-> python bwg_api.py -h  
Options:
  -h, --help            show this help message and exit
  -c FUNC, --call=FUNC  [start, stop, restart, kill, getServiceInfo,
                        getLiveServiceInfo, getAvailableOS, reinstallOS,
                        resetRootPassword, getUsageGraphs, getRawUsageStats,
                        setHostname, setPTR, basicShell_cd, basicShell_exec,
                        shellScript_exec, snapshot_create, snapshot_list,
                        snapshot_delete, snapshot_restore,
                        snapshot_toggleSticky, snapshot_export,
                        snapshot_import, ipv6_add, ipv6_delete,
                        migrate_getLocations, migrate_start,
                        cloneFromExternalServer, getSuspensionDetail,
                        unsuspend, getRateLimitStatus, help]
  -f FILENAME, --file=FILENAME
                        Assign config file
  --init-config=INIT_CONFIG
                        Init config file
  -e EMAIL, --email=EMAIL
                        email adders,e.g: a@mail.com,b.mail.com
  -m MONITOR, --monitor=MONITOR
                        start monitor
  -r RATE, --rate=RATE  Usage monitoring, email send threshold, e.g: 50%
  
  -> python bwg_api.py -c help
start                    : 	Starts the VPS
stop                     : 	Stops the VPS
restart                  : 	Reboots the VPS
kill                     : 	Allows to forcibly stop a VPS that is stuck and cannot be stopped by normal means
getServiceInfo           : 	Get service info
getLiveServiceInfo       : 	Get all data provided by getServiceInfo
getAvailableOS           : 	Currently installed Operating System
reinstallOS              : 	Reinstall the Operating System
resetRootPassword        : 	Generates and sets a new root password
getUsageGraphs           : 	Obsolete, use getRawUsageStats instead
getRawUsageStats         : 	Get a two-dimensional array with the detailed usage statistics shown under Detailed Statistics in KiwiVM
setHostname              : 	Sets new hostname
setPTR                   : 	Sets new PTR (rDNS) record for IP
basicShell_cd            : 	Simulate change of directory inside of the VPS. Can be used to build a shell like Basic shell
basicShell_exec          : 	Execute a shell command on the VPS (synchronously)
shellScript_exec         : 	Execute a shell script on the VPS (asynchronously)
snapshot_create          : 	Create snapshot
snapshot_list            : 	Get list of snapshots
snapshot_delete          : 	Delete snapshot by fileName (can be retrieved with snapshot/list call)
snapshot_restore         : 	Restores snapshot by fileName (can be retrieved with snapshot/list call)
snapshot_toggleSticky    : 	Set or remove sticky attribute ("sticky" snapshots are never purged). Name of snapshot can be retrieved with snapshot/list call – look for fileName variable
snapshot_export          : 	Generates a token with which the snapshot can be transferred to another instance
snapshot_import          : 	Imports a snapshot from another instance identified by VEID and Token
ipv6_add                 : 	Assigns a new IPv6 address
ipv6_delete              : 	Releases specified IPv6 address
migrate_getLocations     : 	Get all possible migration locations
migrate_start            : 	Start VPS migration to new location
cloneFromExternalServer  : 	(OVZ only) Clone a remote server or VPS
getSuspensionDetail      : 	Retrieve information related to service suspensions
unsuspend                : 	Clear abuse issue identified by record_id and unsuspend the VPS
getRateLimitStatus       : 	This call allows monitoring this matter
```
## config
``` json
{
        "VEID": "",
        "API_KEY_BWH": "",
        "MAIL_HOST": "",
        "MAIL_USER": "",
        "MAIL_PASS": ""
}
```

## use
``` bash
python bwg_api.py -h 
python bwg_api.py -c  function
python bwg_api.py -m network -e flytrap@mail.com -r 50%  # check 
```
python call


``` bash
pip install bwg-api
```

``` python
from bwg.bwg_api import BWG
bwg = BWG(VEID, API_KEY_BWH)
bwg.__doc__  # doc
func = getattr(bwg, func_name)
func()
```

Welcome to suggest improvements.

[中文文档](./README-CN.md)
