#Dockerfile
FROM ubuntu:xenial
LABEL maintainer="shiki"

RUN apt-get update -y

# Deps
RUN apt-get install -y vim python-pip wget git gnupg flex bison gperf build-essential zip curl subversion pkg-config libglib2.0-dev libgtk2.0-dev libxtst-dev libxss-dev libpci-dev libdbus-1-dev libgconf2-dev libgnome-keyring-dev libnss3-dev lsb-release sudo locales libssl-dev openssl cmake lbzip2 libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libswresample-dev libpostproc-dev

# install webrtc deps
RUN curl https://chromium.googlesource.com/chromium/src/+/master/build/install-build-deps-android.sh?format=TEXT | base64 -d > install-build-deps-android.sh
RUN curl https://chromium.googlesource.com/chromium/src/+/master/build/install-build-deps.sh?format=TEXT | base64 -d > install-build-deps.sh
RUN chmod +x ./install-build-deps.sh
RUN chmod +x ./install-build-deps-android.sh
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
RUN ./install-build-deps.sh --no-chromeos-fonts
RUN ./install-build-deps-android.sh

# depot tools
WORKDIR /
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

RUN echo 'export PATH=$PATH:/depot_tools' >> /root/.bashrc
