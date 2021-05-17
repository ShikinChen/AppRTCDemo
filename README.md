### WebRTC Android的c++源码在mac调试项目 调试方式来源于[WebRTC 学习指南](https://webrtc.mthli.com/basic/webrtc-breakpoint/)和[Flutter Engine C++ 源码调试初探_7. VSCode中使用LLDB调试](https://fucknmb.com/2019/12/06/Flutter-Engine-C-%E6%BA%90%E7%A0%81%E8%B0%83%E8%AF%95%E5%88%9D%E6%8E%A2/),而编译方式和服务器搭建来源于[WebRTC Native 开发实战(许建林)](https://item.jd.com/12939784.html)
<br>

### 编译和服务器搭建都是基于[docker](https://www.docker.com/)  
<br>

### 编译在webrtc目录用终端执行
构建镜像
```
./build_image.sh
```

创建临时容器并且在进入容器bash环境执,<mark>默认使用mac的酸酸乳进行代理端口是1087,不一样进行修改</mark>
```
./webrtc_build.sh #不用代理追加proxy-off参数 例如: ./webrtc_build.sh proxy-off
```

可以选择性更新depot_tools一般第一次创建镜像都会拉取最新
```
cd /webrtc
./depot_tools_update.sh
```

第一次拉取拉取webrtc源码需要加init,以后不需要
```
cd /webrtc
./gclient_sync.sh init
```


如果结合[WebRTC Native 开发实战(许建林)](https://item.jd.com/12939784.html)进行学习最好切换30432的提交并且进行同步
```
cd /webrtc/src
git checkout be99ee8f17f93e06c81e3deb4897dfa8253d3211
cd /webrtc
./gclient_sync.sh
```

### 编译
脚本已经unstrip直接执行打包,会提示ERROR:root:Missing licenses的协议生成错误这个可以不用处理只要生成libjingle_peerconnection_so.so就行,最后libjingle_peerconnection_so.so在<mark>webrtc-build/webrtc_android/src/out/arm64-v8a</mark>  
```
cd /webrtc
./build_android.sh
```
<br> 


### 调试  
先将libjingle_peerconnection_so.so复制到webrtc/prebuilt_libs/arm64-v8a(如果目录不存在自行创建),然后参考[WebRTC 学习指南](https://webrtc.mthli.com/basic/webrtc-breakpoint/)获取so相对c++源码的链接地址,也可以直接用Android studio进行调试,但是c++因为没办法导入生成索引没法进行代码跳转,所以java层用Android studio调试,而c++改用[vscode](https://code.visualstudio.com/)调试思路是按照[Flutter Engine C++ 源码调试初探_7. VSCode中使用LLDB调试](https://fucknmb.com/2019/12/06/Flutter-Engine-C-%E6%BA%90%E7%A0%81%E8%B0%83%E8%AF%95%E5%88%9D%E6%8E%A2/)和[他的flutter_lldb脚本](https://github.com/lizhangqu/flutter_lldb.git)进行改造实现的  
<br>
需要安装以下插件  
[C/C++ for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)  
[CodeLLDB](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb)  
[Android](https://marketplace.visualstudio.com/items?itemName=adelphes.android-dev-ext)  

然后用vscode打开AppRTCDemo目录先手动或者用vscode的Android launch启动app,然后执行start_lldb.sh脚本<mark>第一次使用可能需要修改脚本的 --remote-src-path=../../../ 改为地址为so的软连接,如果按上面步骤打包应该不需要修改</mark>   
然后在vscode选择debug_native启动c++调试,基本每次杀死app都跑start_lldb.sh脚本重启定位pid开启lldb-server
![](./img/1.png)
<br>   
<br>  

### 启动服务器
直接执行项目下的webrtc_server.sh脚本,而且调试项目默认是本机所在局域网的ip,如果服务器不是在本机运行,自行修改build.gradle脚本的pref_room_server_url_default参数值,不过注意运行过一次默认会保存上一次地址
```
./webrtc_server.sh
```

## License

```
Copyright (c) 2021, Matthew Lee
Copyright (c) 2015 - 2021, Taehyun Park
Copyright (c) 2011 - 2021, The WebRTC project authors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
