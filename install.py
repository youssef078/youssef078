#!/usr/bin/env python3

from json import dump, load
from os import environ, mkdir, path, system
from re import match
from shutil import copyfile, copytree, rmtree
from sys import executable, platform, argv
import uuid
from zipfile import ZipFile

def copy():
    MCPYPATH = search_mcpy()
    if not path.isdir(MCPYPATH):
        mkdir(MCPYPATH)
    install_json('settings.json')
    if not path.isdir(path.join(MCPYPATH, 'lib')):
        mkdir(path.join(MCPYPATH, 'lib'))
    if not path.isdir(path.join(MCPYPATH, 'log')):
        mkdir(path.join(MCPYPATH, 'log'))
    if not path.isdir(path.join(MCPYPATH, 'save')):
        mkdir(path.join(MCPYPATH, 'save'))
    if not path.isdir(path.join(MCPYPATH, 'screenshot')):
        mkdir(path.join(MCPYPATH, 'screenshot'))
    if not path.isdir(path.join(MCPYPATH, 'resource-pack')):
        mkdir(path.join(MCPYPATH, 'resource-pack'))
    if path.isdir(path.join(MCPYPATH, 'resource-pack', 'default')):
        rmtree(path.join(MCPYPATH, 'resource-pack', 'default'))
    ZipFile(path.join(get_file('data'), 'pack.zip')).extractall(path.join(MCPYPATH, 'resource-pack'))

def install():
    # 下载依赖项
    if '--no-install-requirements' not in argv:
        print('[(1/3) Install requirements]')
        pip = executable + ' -m pip'
        if '--hide-output' in argv:
            code = system('%s install -U -r %s >> %s' % (pip, get_file('requirements.txt'), path.devnull))
        else:
            code = system('%s install -U -r %s' % (pip, get_file('requirements.txt')))
        if code != 0:
            print('pip raise error code: %d' % code)
            exit(1)
        else:
            print('install successfully')
    else:
        print('[(1/3) Skip install requirements]')
    # 注册玩家
    register_user()
    # 复制运行所需的文件
    print('[(3/3) Copy lib]')
    copy()
    # 完成!
    print('[Done]')

def get_file(f):
    # 返回文件目录下的文件名
    return path.abspath(path.join(path.dirname(__file__), f))

def install_json(f):
    MCPYPATH = search_mcpy()
    source = load(open(path.join(get_file('data'), f)))
    target = {}
    if path.isfile(path.join(MCPYPATH, f)):
        target = load(open(path.join(MCPYPATH, f)))
    else:
        target = {}
    for k, v in source.items():
        if k not in target:
            target[k] = v
    dump(target, open(path.join(MCPYPATH, f), 'w+'))

def register_user():
    # 注册
    if '--skip-register' not in argv:
        print('[(2/3) Register]')
        MCPYPATH = search_mcpy()
        if not path.isdir(MCPYPATH):
            mkdir(MCPYPATH)
        if not path.isfile(path.join(MCPYPATH, 'player.json')):
            player_id = str(uuid.uuid4())
            print('Your uuid is %s, do not change it' % player_id)
            player_name = ''
            while not match(r'^([a-z]|[A-Z]|_)\w+$', player_name):
                player_name = input('Your name: ')
            dump({'id': player_id, 'name': player_name}, open(path.join(MCPYPATH, 'player.json'), 'w+'), indent='\t')
            print('Regsitered successfully, you can use your id to play multiplayer game!')
        else:
            print('You have regsitered!')
    else:
        print('[(2/3) Skip regsiter]')

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

if __name__ == '__main__':
    install()
