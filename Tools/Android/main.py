import os,sys,shutil,time,stat


def prepare():
    print("prepare")
    if not os.path.exists("./packConfig.json"):
        shutil.copy('./resources/packConfig.json.template','./packConfig.json')
    print("prepare...ok")
    print("Modify the permissions ")
    filesChmod(os.path.abspath(os.path.dirname(__file__)))
    # os.chmod("packConfig.json",stat.S_IWRITE)
    print("Modify the permissions...ok ")
    time.sleep(2)
#修改当前目录中所有文件的权限
def filesChmod(filepath):
  files = os.listdir(filepath)
  for fi in files:
    fi_d = os.path.join(filepath,fi)            
    if os.path.isdir(fi_d):
       filesChmod(fi_d)                  
    else :
       os.chmod(fi_d,stat.S_IWRITE)
    #    print("modify "+fi_d.split("\\")[-1]+"permissions   ok")    
   

if __name__ == "__main__":
    isprepared=False
    targetDir=os.path.abspath(os.path.dirname(__file__))
    os.chdir(targetDir)
    try:
        prepare()
        isprepared=True
    except:
        isprepared=False
        print("prepare...failed")
    print("please check your packConfig message before running,Go ahead ? [Yes/No] ")
    while(1):
        u_input=input()
        if  isinstance(u_input,str):
            if str.upper(u_input)=="YES" or str.upper(u_input)[0]=="Y" :
                isprepared and os.system("python ./resources/packing.py")
                time.sleep(1)
                break
            else:
                break    
        
    
   