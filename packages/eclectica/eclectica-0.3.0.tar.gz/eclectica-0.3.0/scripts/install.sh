#!/bin/sh

install () {

set -eu

UNAME=$(uname)
if [ "$UNAME" != "Linux" -a "$UNAME" != "Darwin" ] ; then
    echo "Sorry, OS not supported: ${UNAME}. Download binary from https://github.com/markelog/eclectica/releases"
    exit 1
fi

if [ "$UNAME" = "Darwin" ] ; then
  OSX_ARCH=$(uname -m)
  if [ "${OSX_ARCH}" = "x86_64" ] ; then
    PLATFORM="darwin_amd64"
  else
    echo "Sorry, architecture not supported: ${OSX_ARCH}. Download binary from https://github.com/markelog/eclectica/releases"
    exit 1
  fi
elif [ "$UNAME" = "Linux" ] ; then
  LINUX_ARCH=$(uname -m)
  if [ "${LINUX_ARCH}" = "x86_64" ] ; then
    PLATFORM="linux_amd64"
  else
    echo "Sorry, architecture not supported: ${LINUX_ARCH}. Download binary from https://github.com/markelog/eclectica/releases"
    exit 1
  fi
fi

if [ -n "${EC_VERSION+set}" ] ; then
  VERSION=v$EC_VERSION
else
  VERSION=$(curl -s https://api.github.com/repos/markelog/eclectica/tags | grep -Eo '"name":.*?[^\\]",'  | head -n 1 | sed 's/[," ]//g' | cut -d ':' -f 2)
fi

if [ -n "${EC_DEST+set}" ] ; then
  DEST=$EC_DEST
else
  DEST=/usr/local/bin
fi

DEST_MAIN="$DEST/ec"
DEST_PROXY="$DEST/ec-proxy"
MAIN="https://github.com/markelog/eclectica/releases/download/$VERSION/ec_$PLATFORM"
PROXY="https://github.com/markelog/eclectica/releases/download/$VERSION/ec-proxy_$PLATFORM"

if [ -z $VERSION ] ; then
  echo "Error requesting. Download binary from https://github.com/markelog/eclectica/releases"
  exit 1
else
  echo "\nDownloading main binary\n"
  curl -L $MAIN -o $DEST_MAIN

  echo "\nDownloading proxy binary\n"
  curl -L $PROXY -o $DEST_PROXY

  chmod +x $DEST_MAIN $DEST_PROXY
fi

}

install
