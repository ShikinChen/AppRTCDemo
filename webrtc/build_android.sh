#!/bin/sh
SHELL_PATH=$(pwd)
SRC_PATH=$SHELL_PATH/src
OUT_PATH=$SRC_PATH/out/android_debug
ANDROID_BUILD_PATH=$SRC_PATH/build/toolchain/android/BUILD.gn

if [ ! -d "$OUT_PATH" ]; then
  mkdir -p $OUT_PATH
fi

if [ ! -f "${ANDROID_BUILD_PATH}_bak" ]; then
  cp $ANDROID_BUILD_PATH ${ANDROID_BUILD_PATH}_bak
fi

sed -i "/strip = rebase_path/d" $ANDROID_BUILD_PATH
sed -i "/         root_build_dir)/d" $ANDROID_BUILD_PATH
sed -i "/use_unstripped_as_runtime_outputs = android_unstripped_runtime_outputs/d" $ANDROID_BUILD_PATH

cd $SRC_PATH && $SRC_PATH/tools_webrtc/android/build_aar.py --extra-gn-args "is_debug=true symbol_level=2 android_full_debug=true" --arch arm64-v8a --build-dir $OUT_PATH --out $OUT_PATH/libwebrtc.aar
