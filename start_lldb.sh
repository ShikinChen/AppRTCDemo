#! /bin/sh
SHELL_PATH=$(pwd)

$SHELL_PATH/android_lldb.py --remote-src-path=../../../ \
--local-src-path=$SHELL_PATH/webrtc/webrtc_android/src \
--launch-path=$SHELL_PATH/.vscode/launch.json \
org.appspot.apprtc
