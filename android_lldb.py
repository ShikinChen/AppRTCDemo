#!/usr/bin/env python
# coding=utf-8

import argparse
import os
import re
import subprocess
import sys
import json

from scipy.weave.converters import default

def _find_package_pid(adb_path, package):
    """Find the pid of the Flutter application process."""
    ps_output = subprocess.check_output([adb_path, 'shell', 'ps'])
    ps_match = re.search('^\S+\s+(\d+).*\s%s' % package, ps_output, re.MULTILINE)
    if not ps_match:
        print 'Unable to find pid for package %s on device' % package
        print 'You can get the application pid by execute one of the commands in terminal:'
        print 'adb shell pidof %s' % package
        print 'adb shell ps | grep %s | awk \'{ print $2 }\'' % package
        print ''
        return None
    return int(ps_match.group(1))


def _get_android_home(args):
    """get the android sdk home."""
    android_sdk = args.android_sdk
    if android_sdk and os.path.exists(android_sdk):
        return android_sdk
    android_home = os.getenv("ANDROID_HOME")
    if not android_home:
        raise EnvironmentError(
            "You must set environment with $ANDROID_HOME or provide the android sdk home with --android-sdk")
    return android_home


def _get_adb_path(args):
    """get the adb path."""
    return os.path.join(_get_android_home(args), "platform-tools", "adb")

def main():
    parser = argparse.ArgumentParser(description='lldb debugger tool')
    parser.add_argument('--abi', type=str, choices=['armeabi', 'arm64-v8a', 'x86', 'x86_64'],
                        help="lldb-server使用的abi", default="arm64-v8a")
    parser.add_argument('--android-sdk', type=str, help="android sdk路径默认用环境变量ANDROID_HOME")
    parser.add_argument('--local-src-path', type=str, required=True,
                        help="c++源码路径")
    parser.add_argument('--remote-src-path', type=str,
                        help="so对应的c++链路径", required=True, )
    parser.add_argument('--as-path', type=str, help='Android Studio路径', default="/Applications/Android Studio.app")
    parser.add_argument('--launch-path', type=str, help='vscode的launch.json路径,一般当前项目的.vscode/launch.json')
    parser.add_argument('package', type=str, help="app包路径")
    return run(parser.parse_args())


def run(args):
    adb_path = _get_adb_path(args)
    # 根据app包路径获取app线程id
    application_pid = _find_package_pid(adb_path, args.package)
    pid = application_pid or (
            'get pid by execute `adb shell pidof %s` yourself' % args.package)

    if not application_pid:
        print "app还没启动,先启动app"
        print ''

    json_config = {}
    if args.launch_path and os.path.exists(args.launch_path):
        f = open(args.launch_path)
        text = f.read()
        f.close()
        json_config = json.loads(text)
    else:
        text = """
        {
            "version": "0.2.0",
            "configurations": [
            ]
        }
        """
        json_config = json.loads(text)

    lldb_config_name = "debug_native"
    lldb_config = """
            {
                "name": "%s",
                "type": "lldb",
                "request": "attach",
                "pid": "%s",
                "initCommands": [
                    "platform select remote-android",
                    "platform connect unix-abstract-connect:///%s/debug.socket"
                ],
                "postRunCommands": [
                    "settings set target.source-map %s %s"
                ]
            }
        """ % (lldb_config_name,
               pid, args.package, args.remote_src_path,
               args.local_src_path)

    lldb_config_json = json.loads(lldb_config)
    is_lldb_config_exist = False
    configurations_key = "configurations"
    for index in range(len(json_config[configurations_key])):
        value = json_config[configurations_key][index]
        if value["name"] == lldb_config_name:
            is_lldb_config_exist = True
            json_config[configurations_key][index] = lldb_config_json
            break

    if not is_lldb_config_exist:
        json_config[configurations_key].append(lldb_config_json)

    contents_dir = ""
    # 判断是否mac系统
    if sys.platform == "darwin":
        contents_dir = "Contents"
    # 从Android Studio获取lldb-server和启动脚本复制到/data/local/tmp
    lldb_server_local_dir_path = "%s/%s/bin/lldb/android" % (args.as_path, contents_dir)

    tmp_dir_path = "/data/local/tmp"

    subprocess.check_call(
        [adb_path, 'push', "%s/start_lldb_server.sh" % lldb_server_local_dir_path, tmp_dir_path])

    subprocess.check_call(
        [adb_path, 'push', "%s/%s/lldb-server" % (lldb_server_local_dir_path, args.abi), tmp_dir_path])

    # 将/data/local/tmp/lldb-server 复制到相应应用的目录
    lldb_server_dir_path = '/data/data/%s/lldb' % args.package

    lldb_server_bin_path = '%s/bin' % lldb_server_dir_path

    subprocess.check_call(
        [adb_path, 'shell', 'run-as', args.package, 'mkdir', '-p',
         lldb_server_bin_path])

    lldb_server_path = '%s/lldb-server' % lldb_server_bin_path

    subprocess.check_call(
        [adb_path, 'shell', 'run-as', args.package, 'cp', '-F',
         "%s/lldb-server" % (
             tmp_dir_path), lldb_server_path])

    subprocess.check_call([adb_path, 'shell', 'run-as', args.package, 'chmod', 'a+x', lldb_server_path])

    lldb_server_sh_path = '%s/start_lldb_server.sh' % lldb_server_bin_path

    subprocess.check_call(
        [adb_path, 'shell', 'run-as', args.package, 'cp', '-F',
         "%s/start_lldb_server.sh" % (
             tmp_dir_path), lldb_server_sh_path])

    subprocess.check_call([adb_path, 'shell', 'run-as', args.package, 'chmod', 'a+x', lldb_server_sh_path])
    # 杀掉之前的lldb-server线程
    subprocess.call([adb_path, 'shell', 'run-as', args.package, 'killall', 'lldb-server'])

    json_text = json.dumps(json_config, indent=4)
    if not args.launch_path:
        print("")
        print("没有配置launch.json路径请自行复制下面代码到launch.json:\n\n%s" % json_text)
    else:
        f = open(args.launch_path, "w")
        f.write(json_text)
        f.close()

    # 启动lldb-server
    subprocess.check_call([adb_path, 'shell', 'run-as', args.package, 'sh', '-c',
                           "'%s /data/data/%s/lldb unix-abstract /%s debug.socket \"lldb process:gdb-remote packets\"'" % (
                               lldb_server_sh_path, args.package, args.package)])

    return 0


if __name__ == '__main__':
    sys.exit(main())
