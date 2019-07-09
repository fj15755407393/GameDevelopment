#!/user/bin/python
# coding=utf-8
import subprocess
import stat
import time
import json
import sys
import os
import datetime
import shutil
# 初始化变量

scriptPath = os.path.dirname(os.path.abspath(__file__))
scriptPath = scriptPath.replace('\\', '/')
exportPath = os.path.abspath("../../Output/Android")  # 导出目录
extraProjectData = ''
unityPath = ''
projectPath = ''
jrePath = ''
companyName = ''
productName = ''
deleteAssets = []


# 切换工作目录
if not os.getcwd().replace('\\', '/') == scriptPath:
    os.chdir(scriptPath)


# 加载配置信息
print("Load configuration information...")
with open('../packConfig.json', 'r+') as fp:
    packConfig = json.load(fp)

try:
    unityPath = packConfig['unityPath']
    projectPath = packConfig['projectPath']
    jrePath = packConfig['jrePath']
    companyName = packConfig['companyName']
    productName = packConfig['productName']
    deleteAssets = packConfig['deleteAssets']
    deleteGradle = packConfig['deleteGradle']
except Exception:
    print("update variable failed ,please check the packConfig.json message")
    quit()


print("Load configuration information...completed")


# 作为版本号
now_time = datetime.datetime.now().strftime(productName + '-%Y%m%d-%H%M')

exportPath = exportPath + '/' + now_time
logpath = '../log/' + now_time + '.log'
temp_now = datetime.datetime.now()

# 如果导出目录不存在则创建
if not os.path.exists(exportPath):
    os.makedirs(exportPath)

# 打包失败时调用 删除生成的文件


def deleteTemp():
    os.chdir(scriptPath)
    shutil.rmtree(exportPath)
    quit()
# 删除多余的音频文件 /Assets/StreamingAssets/Audio/GeneratedSoundBanks 路径下的
otherPath = projectPath + "/Assets/StreamingAssets/Audio/GeneratedSoundBanks"
if os.path.exists(otherPath):
    folders = os.listdir(otherPath)
    for folder in folders:
        if not (("Android" in folder) or ("Wwise_IDs.h" in folder)):
            dir = otherPath + '/' + folder
            if os.path.isdir(dir):
                shutil.rmtree(dir)
                os.remove(os.path.abspath(dir) + ".meta")
    print("\nDelete other Audio Files...Completed")


# 如果jre/lib 中没有tools.jar 则拷贝一份
if not os.path.exists(jrePath + '/tools.jar'):
    try:
        shutil.copy('./tools.jar', jrePath)
    except:
        print('tools.jar copy failed, you can select : \n'
              + '[1] run the script by administrator \n'
              + '[2] Manually copy the tools.jar into the jre/lib directory ')
        deleteTemp()

# 利用unity导出工程
print('export gradle project...')

result = subprocess.call(unityPath + " -quit " + " -batchmode " + " -logFile " + logpath +
                         " -projectPath " + projectPath + " -executeMethod  AutoBuild.BuildForAndroid  -outputPath " + exportPath + " " + productName + " " + companyName)

# result:0 suceessful other failed
if result == 0:
    print('export gradle project...completed')
    os.chdir(exportPath + '/' + productName)
else:
    print('export gradle project...failed')
    print(" maybe unity script compilation failed please check it in log")
    deleteTemp()

# 删除AndroidManifest.xml 中获取地理位置权限
xmlPath=exportPath+"/IrisFall/src/main/AndroidManifest.xml"
if os.path.exists(xmlPath):
    print(" delete android.permission.ACCESS_FINE_LOCATION...")
    with open(xmlPath,"r+") as fr:
        lines=fr.readlines()
    with open(xmlPath,"w")  as fw:
        for line in lines:
            if '"android.permission.ACCESS_FINE_LOCATION"' in line:
                continue 
            fw.write(line)
    print("delete android.permission.ACCESS_FINE_LOCATION...ok")          

# 删除资源文件 快速打包
print('delete assets files')
try:
    for da in deleteAssets:
        shutil.rmtree('src/main/assets/' + da)
        print('delete directory {0}...ok'.format(da))
except Exception:
    print('there are not ' + da)

print('delete assets files...completed')

# 拷贝依赖库
os.chdir(scriptPath)
libPath = os.path.abspath('./jniLibs').replace("\\", "/")
# print('libPath: ' + libPath)

if os.path.exists(libPath):
    print('copy lib...')
    list = os.listdir(libPath + '/armeabi-v7a')
    for i in range(0, len(list)):
        filePath = os.path.join(libPath + '/armeabi-v7a',
                                list[i]).replace('\\', '/')
        if os.path.isfile(filePath):
            shutil.copy(filePath, exportPath +
                        '/' + productName + '/src/main/jniLibs/armeabi-v7a')
            print('     ' + list[i] + ' ok')

    list = os.listdir(libPath + '/x86')
    for i in range(0, len(list)):
        filePath = os.path.join(libPath + '/x86', list[i])
        if os.path.isfile(filePath):
            shutil.copy(filePath, exportPath +
                        '/' + productName + '/src/main/jniLibs/x86')
            print('     ' + list[i] + ' ok')
    print('copy lib...completed')

# gradle android 工程
os.chdir(exportPath + '/' + productName)
print('gradle android project...')
while(True):

    result = os.system('gradle  assembleDebug')
    if result == 0:
        print('gradle android project...completed')
        break
    else:
        print("gradle failed, you can try install gradle and Add it to the environment variable or check the SDK path ,\n" +
              "You can  modify the SDK path in several ways :\n" +
              "[1] change the Unity Preferences-Extermal Tools-Android-SDK \n" +
              "[2] Edit the " + exportPath + '/' + productName + "/local.properties file\n" +
              "[3] change the Android Studio File-settings-System Settings-Android SDK-Android SDK Location if you installed Android Studio")
        # time.sleep(1)
        # u_input=input("if you are sure that you have resolved the gradle problem, you can choose to continue or exit,Continue ? [Yes/No] \n")
        # if  isinstance(u_input,str):
        #      if str.upper(u_input)[0]=="Y" :
        #           commands=
        #           os.system(" start cmd")
        #           continue
        #           time.sleep(1)

        #      else:
        #           shutil.rmtree(exportPath)
        #           quit()
        deleteTemp()


# 删除gradle文件只保存apk文件
if not deleteGradle == "False":
    os.chdir(scriptPath)
    sourcePath = exportPath + '/' + productName + \
        '/build/outputs/apk/debug/' + productName + '-debug.apk'
    targetPath = exportPath + '/' + now_time + '.apk'
    print('collating files...')
    shutil.copy(sourcePath, targetPath)
    shutil.rmtree(exportPath + '/' + productName)
    print('collating files...completed')

temp_end = datetime.datetime.now()
print('Script executed successfully ! the appplication version is {0} , elapsed time {1} '.format(
    now_time, str(temp_end - temp_now).split('.')[0]))
