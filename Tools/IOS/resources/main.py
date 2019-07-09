import os,sys,shutil,time,stat


def prepare():
    print("prepare")

    # print("Modify the permissions ")
    # os.system("chmod -R 754 "+os.path.abspath(os.path.dirname(__file__)))
    # filesChmod(os.path.abspath(os.path.dirname(__file__)))
    # os.chmod("packConfig.json",stat.S_IWRITE)
    # print("Modify the permissions...ok ")
    time.sleep(2)

   

if __name__ == "__main__":
    isprepared=False
    targetDir=os.path.abspath(os.path.dirname(__file__))
    os.chdir(targetDir)
    os.system("python3 ./IosPacking.py")
    # try:
    #     prepare()
    #     isprepared=True
    # except:
    #     isprepared=False
    #     print("prepare...failed")
    # # print("please check your packConfig message before running,Go ahead ? [Yes/No] ")
    # while(1):
    #     u_input=input()
    #     if  isinstance(u_input,str):
    #         if str.upper(u_input)=="YES" or str.upper(u_input)[0]=="Y" :
                
    #             isprepared and os.system("python3 ./packing.py")
    #             time.sleep(1)
    #             break
    #         else:
    #             break    
        
    
   