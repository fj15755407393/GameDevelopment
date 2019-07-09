import json
import os
import sys
import shutil
import stat
import getpass
# 切换工作目录

# 获取当前用户
user = getpass.getuser()

if not user == 'root':
    print('please run the script by root')
    quit()

if not os.path.exists("./packConfig.json"):
    shutil.copy('./resources/packConfig.json.template', './packConfig.json')

with open('./packConfig.json', 'r+') as fp:
    config = json.load(fp)

project_path = config['project_path']
permissions_arget = config['permissions_arget']

# 修改文件夹权限
os.system('chmod -R 777 ' + permissions_arget)
