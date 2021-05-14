#! /bin/sh
SHELL_PATH=$(pwd)
WEBRTC_PATH=/webrtc

if [ -f "$WEBRTC_PATH/.boto" ]; then
  export NO_AUTH_BOTO_CONFIG=$WEBRTC_PATH/.boto
fi

if [ -n "$1" ]; then
  if [ $1 = "clean" ]; then
    BUILD_PATH=$WEBRTC_PATH/src/build
    if [ -d "$BUILD_PATH" ]; then
      rm -rf $BUILD_PATH
    fi

    THIRD_PARTY_PATH=$WEBRTC_PATH/src/third_party
    if [ -d "$THIRD_PARTY_PATH" ]; then
      rm -rf $THIRD_PARTY_PATH
    fi
  fi
  if [ $1 = "init" ]; then
    cd /webrtc && fetch --nohooks webrtc_android
  fi
else
  cd /webrtc && gclient sync -v -D
fi
