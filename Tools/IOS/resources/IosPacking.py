#!/user/bin/python
# coding=utf-8
import subprocess,stat,time,json,sys,os
import datetime
import shutil
# 初始化变量

script_path = os.path.dirname(os.path.abspath(__file__))
script_path = script_path.replace('\\', '/')
xcode_path = os.path.abspath("../../../Output/IOS")#导出目录

unity_path=''
project_path=''
jrePath=''
company_name=''
product_name=''

ipa_path=""

vars_list=globals()

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

# os.system("chmod -R 777 "+project_path)

# 作为版本号
now_time = datetime.datetime.now().strftime(product_name+'-%Y%m%d-%H%M')

xcode_path = xcode_path + '/' + now_time
log_path = '../log/' + now_time + '.log'
temp_now = datetime.datetime.now()

# 如果导出目录不存在则创建
if not os.path.exists(xcode_path):
    os.makedirs(xcode_path)

#打包失败时调用 删除生成的文件
def deleteTemp():
     os.chdir(script_path)
     shutil.rmtree(xcode_path)  
     quit()
 
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
print('export xcode project...')
# os.system('su - minliu')
result=os.system(unity_path+ " -quit " + " -batchmode " + " -logFile " + log_path +" -projectPath " + project_path + " -executeMethod  AutoBuild.BuildForIOS  -outputPath " + xcode_path+" "+product_name+" "+company_name)


# result:0 suceessful other failed
if result==0:
    print('export xcode project...completed')
#     os.system("chmod -R 754 "+exportPath)
    os.chdir(xcode_path + '/')
else:
    print('export xcode project...failed')
    print(" maybe unity script compilation failed please check it in log")
    deleteTemp()     


CODE_SIGN_IDENTITY = "iPhone Distribution: companyname (9xxxxxxx9A)"
PROVISIONING_PROFILE = "9437eead-6b68-4288-9235-60c47e4f35d0"

SDK = "iphoneos"


os.system("python3 "+script_path+"/build.py  "+xcode_path+" "+product_name+" "+now_time)



temp_end = datetime.datetime.now()
print('Script executed successfully ! the appplication version is {0} , elapsed time :{1} '.format(now_time, str(temp_end - temp_now).split('.')[0]))


