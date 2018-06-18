#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
import os
import optparse
import requests
import functools
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

LANG = None


def _doc(func: str):
    """
    获取单个方法文档说明
    :param func: 函数名
    :return:
    """
    li = func.split('_')
    doc = BWG.get_api_dict().get(li[0])
    func_doc = doc
    if isinstance(doc, dict):
        func_doc = doc.get(li[-1])
    api_params = BWG.get_api_params()
    fun_params = api_params.get(func)
    text = '\n'.join([f'{k}: \t{v}' for k, v in fun_params.items()])
    eg = ' '.join([f'{k}={v}' for k, v in fun_params.items()])
    return f'{func_doc}\nparams:\n {text}\ne.g: {func} {eg}'


def _docs():
    """
    获取全部文档
    :return:
    """
    content = ''
    for k, v in BWG.get_api_dict().items():
        if isinstance(v, dict):
            content += ''.join([f'{"_".join([k, f]):<25}: \t{t}\n' for f, t in v.items()])
            continue
        content += f'{k:<25}: \t{v}\n'
    return content


def _get_lang():
    """
    获取系统语言
    :return:
    """
    global LANG
    if not LANG:
        LANG = 'cn' if 'cn' in os.environ.get('LANG', 'en').lower() else 'en'
    return LANG


def get_default_config_path():
    """获取默认配置文件路径"""
    home = os.environ.get('HOME')
    rc1 = os.path.join(home, '.config', 'bwg', 'bwgrc')
    rc2 = os.path.join(home, '.bwgrc')
    return rc1, rc2


def _read_config(file_path=None):
    """读取配置文件"""
    global VEID, API_KEY_BWH, MAIL_HOST, MAIL_USER, MAIL_PASS

    def read_config(filename):
        # 读取配置文件
        print('read config...')
        global VEID, API_KEY_BWH, MAIL_HOST, MAIL_USER, MAIL_PASS
        with open(filename) as f:
            config = json.loads(f.read())
            VEID = config.get('VEID')
            API_KEY_BWH = config.get('API_KEY_BWH')
            MAIL_HOST = config.get('MAIL_HOST', '')
            MAIL_USER = config.get('MAIL_USER', '')
            MAIL_PASS = config.get('MAIL_PASS', '')

    if file_path:
        if os.path.exists(file_path):
            return read_config(file_path)
        print(f'{file_path} is not found!!!')
        exit(0)

    rc1, rc2 = get_default_config_path()
    if os.path.exists(rc1):
        read_config(rc1)
    elif os.path.exists(rc2):
        read_config(rc2)
    else:
        VEID = os.environ.get('VEID', '')
        API_KEY_BWH = os.environ.get('API_KEY_BWH', '')
        MAIL_HOST = os.environ.get('MAIL_HOST', '')
        MAIL_USER = os.environ.get('MAIL_USER', '')
        MAIL_PASS = os.environ.get('MAIL_PASS', '')


def init_config(file_path=None):
    """初始化配置文件"""
    config_text = '{\n\t"VEID": "",\n\t"API_KEY_BWH": "",\n\t"MAIL_HOST": "",\n\t"MAIL_USER": "",\n\t"MAIL_PASS": ""\n}'
    if not file_path:
        rc1, rc2 = get_default_config_path()
        if os.path.exists(os.path.dirname(os.path.dirname(rc1))):
            if not os.path.exists(os.path.dirname(rc1)):
                os.mkdir(os.path.dirname(rc1))
            file_path = rc1
        else:
            file_path = rc2
    if os.path.exists(os.path.dirname(file_path)):
        with open(file_path, 'w') as f:
            f.write(config_text)
        print(f'write config file: {file_path}')
    else:
        print('Not found file path')


def send_mail(receivers: [str], subject, text):
    """
    发送邮件
    :param receivers: 接收邮箱
    :param subject: 主题
    :param text: 消息内容
    :return:
    """
    message = MIMEText(f'{text}', 'plain', 'utf-8')
    message['From'] = Header(MAIL_USER, 'utf-8')
    message['To'] = Header(f"{''.join(receivers)}", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        obj = smtplib.SMTP()
        obj.connect(MAIL_HOST, 25)
        obj.login(MAIL_USER, MAIL_PASS)
        obj.sendmail(MAIL_USER, receivers, message.as_string())
        print(f"Mail send to {receivers} Ok")
    except smtplib.SMTPException:
        print("Error: Mail send Error")


class BWG(object):
    """搬瓦工主类"""
    api = 'https://api.64clouds.com/{version}/{func}'

    api_dict_cn = {
        'start': '启动',
        'stop': '停止',
        'restart': '重启',
        'kill': '强制关闭',
        'getServiceInfo': '获取服务器信息',
        'getLiveServiceInfo': '获取活动的服务器信息',
        'getAvailableOS': '获取有效的系统',
        'reinstallOS': '重装系统',
        'resetRootPassword': '重置root密码',
        'getUsageGraphs': '获取使用统计信息',
        'getRawUsageStats': '获取原始状态',
        'setHostname': '设置hostname',
        'setPTR': '设置PTR',
        'basicShell': {
            'cd': '模拟修改路径',
            'exec': '命令'
        },
        'shellScript': {
            'exec': '执行脚本'
        },
        'snapshot': {
            'create': '创建快照',
            'list': '获取快照列表',
            'delete': '删除快照',
            'restore': '恢复快照',
            'toggleSticky': '快照开关',
            'export': '快照导出',
            'import': '快照导入',
        },
        'ipv6': {
            'add': '添加ipv6',
            'delete': '删除ipv6'
        },
        'migrate':
            {
                'getLocations': '获取迁移地址',
                'start': '迁移开始'
            },
        'cloneFromExternalServer': '克隆外部服务器',
        'getSuspensionDetail': '获取被暂停详情',
        'unsuspend': '取消暂停',
        'getRateLimitStatus': '获取使用率状态'
    }
    api_dict_en = {
        'start': 'Starts the VPS',
        'stop': 'Stops the VPS',
        'restart': 'Reboots the VPS',
        'kill': 'Allows to forcibly stop a VPS that is stuck and cannot be stopped by normal means',
        'getServiceInfo': 'Get service info',
        'getLiveServiceInfo': 'Get all data provided by getServiceInfo',
        'getAvailableOS': 'Currently installed Operating System',
        'reinstallOS': 'Reinstall the Operating System',
        'resetRootPassword': 'Generates and sets a new root password',
        'getUsageGraphs': 'Obsolete, use getRawUsageStats instead',
        'getRawUsageStats': 'Get a two-dimensional array with the detailed usage statistics shown under Detailed'
                            ' Statistics in KiwiVM',
        'setHostname': 'Sets new hostname',
        'setPTR': 'Sets new PTR (rDNS) record for IP',
        'basicShell': {
            'cd': 'Simulate change of directory inside of the VPS. Can be used to build a shell like Basic shell',
            'exec': 'Execute a shell command on the VPS (synchronously)'
        },
        'shellScript': {
            'exec': 'Execute a shell script on the VPS (asynchronously)'
        },
        'snapshot': {
            'create': 'Create snapshot',
            'list': 'Get list of snapshots',
            'delete': 'Delete snapshot by fileName (can be retrieved with snapshot/list call)',
            'restore': 'Restores snapshot by fileName (can be retrieved with snapshot/list call)',
            'toggleSticky': 'Set or remove sticky attribute ("sticky" snapshots are never purged).'
                            ' Name of snapshot can be retrieved with snapshot/list call – look for fileName variable',
            'export': 'Generates a token with which the snapshot can be transferred to another instance',
            'import': 'Imports a snapshot from another instance identified by VEID and Token',
        },
        'ipv6': {
            'add': 'Assigns a new IPv6 address',
            'delete': 'Releases specified IPv6 address'
        },
        'migrate':
            {
                'getLocations': 'Get all possible migration locations',
                'start': 'Start VPS migration to new location'
            },
        'cloneFromExternalServer': '(OVZ only) Clone a remote server or VPS',
        'getSuspensionDetail': 'Retrieve information related to service suspensions',
        'unsuspend': 'Clear abuse issue identified by record_id and unsuspend the VPS',
        'getRateLimitStatus': 'This call allows monitoring this matter'
    }

    api_params_cn = {
        'reinstallOS': {'os': '系统'},
        'setHostname': {'newHostname': '新hostname'},
        'setPTR': {'ip': 'ip地址', 'ptr': 'PTR'},
        'basicShell_cd': {'currentDir': '当前路径', 'newDir': '新路径'},
        'basicShell_exec': {'command': '命令'},
        'shellScript_exec': {'script': '脚本'},
        'snapshot_create': {'description': '快照描述(可选)'},
        'snapshot_delete': {'snapshot': '快照'},
        'snapshot_restore': {'snapshot': '快照'},
        'snapshot_toggleSticky': {'snapshot': '快照', 'sticky': 'sticky'},
        'snapshot_export': {'snapshot': '快照'},
        'snapshot_import': {'sourceVeid': 'veId', 'sourceToken': 'token'},
        'ipv6_add': {'ip': 'IP地址'},
        'ipv6_delete': {'ip': 'IP地址'},
        'migrate_start': {'location': '迁移位置'},
        'cloneFromExternalServer': {'externalServerIP': '外部ip', 'externalServerSSHport': 'ssh端口',
                                    'externalServerRootPassword': 'root密码'},
        'unsuspend': {'record_id': '记录id'}
    }
    api_params_en = {
        'reinstallOS': {'os': 'os'},
        'setHostname': {'newHostname': 'newHostname'},
        'setPTR': {'ip': 'ip', 'ptr': 'PTR'},
        'basicShell_cd': {'currentDir': 'currentDir', 'newDir': 'newDir'},
        'basicShell_exec': {'command': 'command'},
        'shellScript_exec': {'script': 'script'},
        'snapshot_create': {'description': 'description (optional)'},
        'snapshot_delete': {'snapshot': 'snapshot'},
        'snapshot_restore': {'snapshot': 'snapshot'},
        'snapshot_toggleSticky': {'snapshot': 'snapshot', 'sticky': 'sticky'},
        'snapshot_export': {'snapshot': 'snapshot'},
        'snapshot_import': {'sourceVeid': 'sourceVeid', 'sourceToken': 'sourceToken'},
        'ipv6_add': {'ip': 'IP'},
        'ipv6_delete': {'ip': 'IP'},
        'migrate_start': {'location': 'location'},
        'cloneFromExternalServer': {'externalServerIP': 'externalServerIP', 'externalServerSSHport': 'ssh port',
                                    'externalServerRootPassword': 'root password'},
        'unsuspend': {'record_id': 'record id'}
    }

    vm_type_filter = {
        'setHostname': 'ovz',
        'cloneFromExternalServer': 'ovz'
    }

    def __init__(self, ve_id, api_key):
        self.ve_id = ve_id
        self.api_key = api_key
        self.params = {
            'veid': ve_id,
            'api_key': api_key
        }

    @classmethod
    def get_api_dict(cls) -> dict:
        """根据系统语言获取api字典"""
        api_dict = getattr(cls, 'api_dict_{}'.format(_get_lang()))
        assert api_dict
        return api_dict

    @classmethod
    def get_api_params(cls) -> dict:
        """根据系统语言获取api参数字典"""
        api_params = getattr(cls, 'api_params_{}'.format(_get_lang()))
        assert api_params
        return api_params

    def req(self, func, version='v1', **kwargs):
        """统一封装API请求"""
        if func not in self.get_api_dict():
            return
        params = self.params.copy()
        if kwargs:
            params.update(kwargs)
        api = self.api.format(version=version, func=func)
        print(f'start request: [{api}] ,params: {params}')
        resp = requests.get(api, params=params)
        return resp.json()

    def __getattr__(self, item):
        """
        重写获取属性方法,字典动态获取,针对方法封装
        :param item: 属性
        :return:
        """
        funcs: list = item.split('_')
        if funcs[0] in self.get_api_dict():
            func_name = funcs[0]
            if len(funcs) == 2:
                func_name = '/'.join(funcs)
            return functools.partial(self.req, func=func_name)
        return BWG.__getattr__(self, item)

    @staticmethod
    def get_all_func():
        """获取所有通过getattr定义的方法"""
        funcs = {}
        for func, doc in BWG.get_api_dict().items():
            if isinstance(doc, dict):
                for k, v in doc.items():
                    funcs[f'{func}_{k}'] = v
                continue
            funcs[f'{func}'] = doc
        return funcs

    def monitor_status(self, mails, monitor, rate):
        """
        监控 monitor 状态
        :param mails: 邮箱，逗号分割
        :param monitor: 监控类型，暂时只有流量
        :param rate: 发送邮件筏值
        :return:
        """
        data = self.getServiceInfo()
        if not mails:
            mails = data.get('email')
        used = round(data.get('data_counter') * data.get('monthly_data_multiplier') / (2 ** 30), 2)
        total = round(data.get('plan_monthly_data') * data.get('monthly_data_multiplier') / (2 ** 30), 2)
        usage = round(used / total * 100, 2)
        text = f'{monitor}-{data.get("hostname")}:\nused: \t{used}G\ntotal: \t{total}G\nusage: \t{usage}%'

        print(f'\nMail: {mails}\n{text}')
        if rate:
            try:
                if '%' in rate:
                    rate = float(rate.replace('%', '')) / 100
                rate = float(rate) * 100
                if usage <= rate:
                    return
            except TypeError:
                print(f'{rate} Type Error!!!')
                return
        send_mail(mails.split(','), f'BWG Monitor{data.get("ip_addresses")}', text)


# 动态重写文档
BWG.__doc__ = _docs()


def init_opt():
    """初始化参数解析"""
    parser = optparse.OptionParser(usage='''e.g: check data usage->%prog -m network -e hiddenstat@gmail.com -r 50%''')
    func_names = BWG.get_all_func()
    choices = list(func_names.keys())
    choices.append('help')
    help_text = f'[{", ".join(choices)}]'
    parser.add_option('-c', '--call', dest='func', type='choice', choices=choices, help=help_text)
    parser.add_option('-f', '--file', dest='filename', help='Assign config file')
    parser.add_option('--init-config', dest='init_config', help='Init config file')
    parser.add_option('-e', '--email', dest='email', help='email adders,e.g: a@mail.com,b.mail.com')
    parser.add_option('-m', '--monitor', dest='monitor', help='start monitor')
    parser.add_option('-r', '--rate', dest='rate', help='Usage monitoring, email send threshold, e.g: 50%')
    options, args = parser.parse_args()
    print(args)
    _read_config(options.filename)
    if options.func == 'help':
        print(BWG.__doc__)
        return
    if options.init_config:
        init_config(options.init_config)
        exit(0)
    bwg = BWG(VEID, API_KEY_BWH)
    if options.monitor:
        bwg.monitor_status(options.email, options.monitor, options.rate)
        exit(0)
    if not options.func:
        parser.print_help()
        return
    api_params = BWG.get_api_params()
    fun_params = api_params.get(options.func)
    func = getattr(bwg, options.func)
    if fun_params and len(args) != len(fun_params):
        print(_doc(options.func))
        return
    if args:
        kwargs = {}
        for arg in args:
            li = arg.split('=')
            if len(li) != 2 or li[0] not in fun_params:
                print(_doc(options.func))
                return
            kwargs[li[0]] = li[1]
        results = func(**kwargs)
    else:
        results = func()
    return results


if __name__ == '__main__':
    print(init_opt())
