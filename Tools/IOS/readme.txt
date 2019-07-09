准备工作：
安装 python3
打包IOS：
    unity File-Build Settings-Player Settings 中
    Ientification:
        Bundle Identifier   : appid 一致
        Signing Team ID     : Apple Developer 官网-Account-Membership 中的 Team ID
        Automatically Sign  : 取消勾选（取消自动签名）
        IOS Provisioning Profile : 选择 Browse 选择下载好的证书文件(Apple Developer 官网-Account-Certificates, Identifiers & Profiles 中下载)
    Xcode: 确保 Xcode-Preference-Account 账号与签名中的一致
    在成功出包的文件中提取 ExportOptions.plist 替换./resources/ExportOptions.plist

打包Android：
    安装 gradle 并添加到环境变量中
    unity 的 buildsetting 需要设置 build system 为 gradle 且勾选 export project 选项

关闭 unity 修改配置信息packConfig.json
先用管理员运行 beforeStart.sh
再用一般用户运行 StartIOS.sh 或 StartAndroid.sh

可能遇到的问题：'Unity-iPhone.xcodeproj' does not exist. 原因可能是unity导出失败 或 unity脚本编译错误 修改相关文件夹权限 或 脚本 
             "Unity-iPhone" requires a provisioning profile.和 archive not found at path 'xxx' 
             原因可能是使用了管理员运行 StartIOS.sh 找不到签名证书 使用一般用户 运行
             

              