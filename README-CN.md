# bwg-api
搬瓦工 Api

## 帮助

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
start                    : 	启动
stop                     : 	停止
restart                  : 	重启
kill                     : 	强制关闭
getServiceInfo           : 	获取服务器信息
getLiveServiceInfo       : 	获取活动的服务器信息
getAvailableOS           : 	获取有效的系统
reinstallOS              : 	重装系统
resetRootPassword        : 	重置root密码
getUsageGraphs           : 	获取使用统计信息
getRawUsageStats         : 	获取原始状态
setHostname              : 	设置hostname
setPTR                   : 	设置PTR
basicShell_cd            : 	模拟修改路径
basicShell_exec          : 	命令
shellScript_exec         : 	执行脚本
snapshot_create          : 	创建快照
snapshot_list            : 	获取快照列表
snapshot_delete          : 	删除快照
snapshot_restore         : 	恢复快照
snapshot_toggleSticky    : 	快照开关
snapshot_export          : 	快照导出
snapshot_import          : 	快照导入
ipv6_add                 : 	添加ipv6
ipv6_delete              : 	删除ipv6
migrate_getLocations     : 	获取迁移地址
migrate_start            : 	迁移开始
cloneFromExternalServer  : 	克隆外部服务器
getSuspensionDetail      : 	获取被暂停详情
unsuspend                : 	取消暂停
getRateLimitStatus       : 	获取使用率状态
```

## 配置文件

默认路径: ~/.config/bwg/bwgrc(~/.bwgrc)

``` json
{
        "VEID": "",
        "API_KEY_BWH": "",
        "MAIL_HOST": "邮箱host",
        "MAIL_USER": "发信邮箱",
        "MAIL_PASS": "密码"
}
```

## 使用
``` bash
python -m bwg.bwg_api -h
python bwg_api.py -h 
python bwg_api.py -c  方法名
python bwg_api.py -m network -e flytrap@mail.com -r 50%  # 检查流量使用情况，超过50则发邮件 
```
python call

``` bash
pip install bwg-api
```

``` python
from bwg.bwg_api import BWG
bwg = BWG(VEID, API_KEY_BWH)
bwg.__doc__  # 类文档
func = getattr(bwg, func_name)
func()
```

欢迎您提出改进建议

[英文文档](./README.md)
