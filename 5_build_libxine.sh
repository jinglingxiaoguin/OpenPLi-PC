#!/bin/bash

# Build and install xine-lib.
OLDLIB="libxine2"
LIB="xine-lib-1.2_1.2.11"
PKG="xine-lib-1.2.11"

dpkg -s $OLDLIB | grep -iw ok > /dev/null

# Remove old package libxine2.
if [ $? -eq 0 ]; then
	apt-get -y purge $OLDLIB*
else
	echo "$LIB not installed"
fi

# Remove old source libxine2.
if [ -d xine-lib-* ]; then
	rm -rf xine-lib-*
fi

if [ -d $PKG ]; then
	rm -rf $PKG
fi

# This is release 1.2.11-2.
wget https://launchpadlibrarian.net/587769116/$LIB.orig.tar.xz
tar -xf $LIB.orig.tar.xz
rm $LIB.orig.tar.xz
mv $PKG $PKG+e2pc
if [ -d $PKG+e2pc ]; then
	cp -fv patches/$PKG+e2pc.patch $PKG+e2pc
else
	echo "-----------------------------------------"
	echo "        CHECK INTERNET CONNECTION!"
	echo "-----------------------------------------"
fi

cd $PKG+e2pc
wget https://launchpadlibrarian.net/587769117/$LIB-2.debian.tar.xz
tar -xf $LIB-2.debian.tar.xz
rm $LIB-2.debian.tar.xz
patch -p1 < $PKG+e2pc.patch
echo "-----------------------------------------"
echo "       patch for xine-lib applied"
echo "-----------------------------------------"
dpkg-buildpackage -b -d -uc -us

cd ..
mv *.deb *.changes *.buildinfo $PKG+e2pc

cd $PKG+e2pc
dpkg -i *.deb
cd ..
