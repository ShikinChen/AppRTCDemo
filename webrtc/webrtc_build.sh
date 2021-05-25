#! /bin/sh
SHELL_PATH=$(pwd)
WEBRTC_ANDROID=$SHELL_PATH/webrtc_android

if [ ! -d "$WEBRTC_ANDROID" ]; then
  mkdir $WEBRTC_ANDROID
fi

if [ ! -f "$WEBRTC_ANDROID/gclient_sync.sh" ]; then
  cp "$SHELL_PATH/gclient_sync.sh" "$WEBRTC_ANDROID/gclient_sync.sh"
fi
if [ ! -f "$WEBRTC_ANDROID/depot_tools_update.sh" ]; then
  cp "$SHELL_PATH/depot_tools_update.sh" "$WEBRTC_ANDROID/depot_tools_update.sh"
fi
if [ ! -f "$WEBRTC_ANDROID/build_android.sh" ]; then
  cp "$SHELL_PATH/build_android.sh" "$WEBRTC_ANDROID/build_android.sh"
fi

HOST_IP=$(ifconfig | grep inet | grep -v inet6 | grep -v 127 | cut -d ' ' -f2)
HOST_IP=($HOST_IP)
HOST_IP=${HOST_IP[0]}

PROXY_PORT=1087

BOTO="[Boto]
proxy = ${HOST_IP}
proxy_port = ${PROXY_PORT}"

if [ -f "$WEBRTC_ANDROID/.boto" ]; then
  rm "$WEBRTC_ANDROID/.boto"
fi

PROXY_SET="--env HTTP_PROXY=http://$HOST_IP:${PROXY_PORT} --env HTTPS_PROXY=http://$HOST_IP:${PROXY_PORT} --dns=8.8.8.8 --dns=8.8.4.4"

if [ -n "$1" ]; then
  if [ $1 = "proxy-off" ]; then
    echo "proxy-off"
    PROXY_SET="--dns=8.8.8.8 --dns=8.8.4.4"
  else
    echo "proxy-on"
    echo $BOTO >> "$WEBRTC_ANDROID/.boto"
  fi
else
  echo "proxy-on"
  echo $BOTO >> "$WEBRTC_ANDROID/.boto"
fi
docker run --rm $PROXY_SET -v "$WEBRTC_ANDROID":/webrtc -it webrtc_build
