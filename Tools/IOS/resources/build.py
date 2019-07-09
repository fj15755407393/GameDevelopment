
import os,sys,subprocess
ENTERPRISECODE_SIGN_IDENTITY='iOS Developer: 添豪 康 (添豪 康)'
ENTERPRISEROVISIONING_PROFILE_NAME='9437eead-6b68-4288-9235-60c47e4f35d0'
CONFIGURATION = "Debug"
# 变量
product_name=sys.argv[1]
print("name:"+product_name)
now_time=sys.argv[2]
ipa_name=product_name+"ipa" 
xcode_path=sys.argv[0]
exportOptionsPlist=os.path.dirname(__file__)+'/ExportOptions.plist'

# clean
clean_command="xcodebuild clean -project Unity-iPhone.xcodeproj -scheme Unity-iPhone -configuration {0}".format(CONFIGURATION)
# print(xcode_path)
# os.chdir(xcode_path)
clean_run=os.system(clean_command)
# print(clean_run)

# archive
archive_path='./Archive/'+product_name.split('/')[-1]+'.xcarchive'
archive_command="xcodebuild archive -project Unity-iPhone.xcodeproj -scheme Unity-iPhone -archivePath {0} -configuration {1} ".format(archive_path,CONFIGURATION)
archive_run=os.system(archive_command)
# print(archive_run)

# 生成ipa
ipa_path='./ipa/'
ipa_command='xcodebuild -exportArchive -archivePath  {0}  -exportPath {1}  -exportOptionsPlist {2}'.format(archive_path,ipa_path,exportOptionsPlist)
ipa_run=os.system(ipa_command)
if ipa_run==0:
    os.system('open '+os.path.abspath(ipa_path))
# print(ipa_run)