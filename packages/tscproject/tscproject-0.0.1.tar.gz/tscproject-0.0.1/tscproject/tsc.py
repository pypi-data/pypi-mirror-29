# coding:utf-8
import sys
import subprocess

PY2 = sys.version_info[0] == 2
if PY2:
    input = raw_input


def tsc_project_init():
    pj_name = input("是否要在当前目录创建一个typescript的项目？(y/n):")
    if "y" != pj_name:
        return
    p = subprocess.Popen("git init", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line)
    p.wait()
    print("开始初始化项目脚手架")
    p = subprocess.Popen("git pull https://gitlab.com/parsecTech/quick-start master", shell=True, stdout=subprocess.PIPE
                         , stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line)
    p.wait()
    print("开始安装必须的包")
    p = subprocess.Popen("npm i", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line)
    p.wait()
    print("初始化完成")
    print("更多说明，请访问 https://gitlab.com/parsecTech/quick-start")


if __name__ == '__main__':
    tsc_project_init()
