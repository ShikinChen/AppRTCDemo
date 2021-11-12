#! /bin/sh
SHELL_PATH=$(cd `dirname $0`;pwd)

pid=$(ps -fe | grep 'android_lldb.py' | grep -v grep | awk '{print $2}')

if [[ -n $pid ]]; then
    kill -9 $pid
fi

MIRROR=$1

if [ ! -n "$MIRROR" ]; then
    MIRROR=agoralab
fi

nohup python "$SHELL_PATH/android_lldb.py" --remote-src-path=../../../ \
--local-src-path="$SHELL_PATH/webrtc/webrtc_src/${MIRROR}/src" \
--launch-path="$SHELL_PATH/.vscode/launch.json" \
org.appspot.apprtc > "$SHELL_PATH/python.log" 2>&1 &

# sleep 2s

# cat "$SHELL_PATH/python.log"
