#!/user/bin/python
# coding=utf-8
import subprocess,stat,time,json,sys,os
import datetime
import shutil
# 初始化变量

script_path = os.path.dirname(os.path.abspath(__file__))
script_path = script_path.replace('\\', '/')
export_path = os.path.abspath("../../Output/Android")#导出目录

unity_path=''
project_path=''
jre_path=''
company_name=''
product_name=''
delete_gradle=True




#切换工作目录
if not os.getcwd().replace('\\', '/')==script_path :
     os.chdir(script_path)
     

# 加载配置信息
print("Load configuration information...")
with open('../packConfig.json', 'r+') as fp:
    config = json.load(fp)

try:
     unity_path=config['unity_path']
     project_path=config['project_path']
     jrePath=config['jrePath']
     company_name=config['company_name']
     product_name=config['product_name']
except Exception:
     print("update variable failed ,please check the packConfig.json message")
     quit()


print("Load configuration information...completed")



# 作为版本号
now_time = datetime.datetime.now().strftime(product_name+'-%Y%m%d-%H%M')

export_path = export_path + '/' + now_time
log_path = '../log/' + now_time + '.log'
temp_now = datetime.datetime.now()

# 如果导出目录不存在则创建
if not os.path.exists(export_path):
    os.makedirs(export_path)

#打包失败时调用 删除生成的文件
def deleteTemp():
     os.chdir(script_path)
     shutil.rmtree(export_path)  
     quit()
     
# targetAutoBuildCS = project_path + '/Assets/Editor/AutoBuild.cs'
# os.chmod(targetAutoBuildCS, stat.S_IREAD | stat.S_IWRITE)
# shutil.copy('./AutoBuild.cs', targetAutoBuildCS)
# os.remove(targetAutoBuildCS+".meta")

#如果jre/lib 中没有tools.jar 则拷贝一份
if not os.path.exists(jrePath+ '/tools.jar'):
     try:
          shutil.copy('./tools.jar',jrePath)
     except:
          print('tools.jar copy failed, you can select : \n'
          +'[1] run the script by administrator \n'
          +'[2] Manually copy the tools.jar into the jre/lib directory ')
          deleteTemp()

# 利用unity导出工程
print('export gradle project...')

result=os.system(unity_path+ " -quit " + " -batchmode " + " -logFile " + log_path +
            " -projectPath " + project_path + " -executeMethod  AutoBuild.BuildForAndroid  -outputPath " + export_path+" "+product_name+" "+company_name)

# result:0 suceessful other failed
if result==0:
    print('export gradle project...completed')
    try:
          os.chdir(export_path + '/' +product_name)
    except FileNotFoundError:
         print("export gradle project...failed")   
         print(" maybe unity script compilation failed please check it in log")
         deleteTemp()       
else:
    print('export gradle project...failed')
    print(" maybe unity script compilation failed please check it in log")
    deleteTemp()     
    
# 删除 AndroidManifest.xml 中获取地理位置权限
xml_path=export_path+"/IrisFall/src/main/AndroidManifest.xml"
if os.path.exists(xml_path):
    print(" delete android.permission.ACCESS_FINE_LOCATION...")
    with open(xml_path,"r+") as fr:
        lines=fr.readlines()
    with open(xml_path,"w")  as fw:
        for line in lines:
            if '"android.permission.ACCESS_FINE_LOCATION"' in line:
                continue 
            fw.write(line)
    print("delete android.permission.ACCESS_FINE_LOCATION...ok")          


#删除资源文件 快速打包 
# print('delete assets files')
# try:
#     for da in deleteAssets:
#         shutil.rmtree('src/main/assets/' + da)
#         print('delete directory {0}...ok'.format(da))
# except Exception:
#     print('there are not ' + da)

# print('delete assets files...completed')

# 拷贝依赖库
# os.chdir(script_path)
# lib_path = os.path.abspath('./jniLibs').replace("\\", "/")
# # print('libPath: ' + libPath)

# if os.path.exists(lib_path):
#     print('copy lib...')
#     list = os.listdir(lib_path + '/armeabi-v7a')
#     for i in range(0, len(list)):
#         filePath = os.path.join(lib_path + '/armeabi-v7a',
#                                 list[i]).replace('\\', '/')
#         if os.path.isfile(filePath):
#             shutil.copy(filePath, export_path +
#                         '/'+ product_name+'/src/main/jniLibs/armeabi-v7a')
#             print('     ' + list[i] + ' ok')

#     list = os.listdir(lib_path + '/x86')
#     for i in range(0, len(list)):
#         filePath = os.path.join(lib_path + '/x86', list[i])
#         if os.path.isfile(filePath):
#             shutil.copy(filePath, export_path +
#                         '/'+product_name+'/src/main/jniLibs/x86')
#             print('     ' + list[i] + ' ok')
#     print('copy lib...completed')

# gradle android 工程
os.chdir(export_path + '/' +product_name)
print('gradle android project...')
while(True):
     
     result=os.system('gradle  assembleDebug')
     if result==0:
          print('gradle android project...completed')
          break
     else :
          print("gradle failed, you can try install gradle and Add it to the environment variable or check the SDK path ,\n"+
          "You can  modify the SDK path in several ways :\n"+
               "[1] change the Unity Preferences-Extermal Tools-Android-SDK \n"+
               "[2] Edit the "+export_path + '/' +product_name+"/local.properties file\n"+
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
# if delete_gradle:
#      os.chdir(script_path)
#      sourcePath = export_path + '/'+product_name+'/build/outputs/apk/debug/'+product_name+'-debug.apk'
#      targetPath = export_path + '/' + now_time + '.apk'
#      print('collating files...')
#      shutil.copy(sourcePath, targetPath)
#      shutil.rmtree(export_path + '/'+product_name)
#      print('collating files...completed')

temp_end = datetime.datetime.now()
print('Script executed successfully ! the appplication version is {0} , elapsed time {1} '.format(now_time, str(temp_end - temp_now).split('.')[0]))


