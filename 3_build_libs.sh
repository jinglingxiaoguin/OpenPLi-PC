#!/bin/bash

# To build enigma2 on Ubuntu 22.04 with startup option "Ubuntu on Xorg".

apt purge -y python2* libpython2*

echo ""
echo "                       *** INSTALL REQUIRED PACKAGES ***"
echo ""

release=$(lsb_release -a 2>/dev/null | grep -i release | awk ' { print $2 } ')

REQPKG_ALL="ant aptitude autoconf automake autopoint avahi-daemon bash build-essential checkinstall chrpath cmake coreutils cvs debhelper desktop-file-utils docbook-utils \
	diffstat dvb-apps dvdbackup ethtool fakeroot flex ffmpeg gawk gettext git help2man linux-headers-`uname -r` libdvdnav-dev libfreetype6-dev libfribidi-dev libsigc++-2.0-dev \
	libpcsclite-dev libjpeg8-dev libgif-dev libjpeg-turbo8-dev libgiftiio0 libaio-dev libxinerama-dev libxt-dev libasound2-dev libcaca-dev libpulse-dev libvorbis-dev \
	libgtk2.0-dev libtool libxml2-dev libxml2-utils libxslt1-dev libssl-dev libvdpau-dev libcdio-dev libcrypto++-dev libudf-dev libvcdinfo-dev libusb-1.0-0-dev \
	libavcodec-dev libavformat-dev libpostproc-dev libavutil-dev libnl-3-dev libbluray-dev libmpcdec-dev libvpx-dev libnl-genl-3-dev libavahi-client3 libavahi-client-dev \
	libflac-dev libogg-dev libxcb-xv0-dev libxcb-shape0-dev libxv-dev libxvmc-dev libaa1-dev libmodplug-dev libjack-jackd2-dev libdirectfb-dev libmagickwand-dev \
	libwavpack-dev libspeex-dev libmng-dev libmad0-dev librsvg2-bin libtheora-dev libsmbclient-dev liblircclient-dev librtmp1 libmng2 libx11-6 libxext6 libglib2.0-dev \
	libelf-dev libmysqlclient-dev libupnp-dev libgiftiio-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev gstreamer1.0-libav mawk mercurial mingetty mjpegtools \
	net-tools openssh-sftp-server pmccabe patch pkg-config rpl rsyslog rtmpdump sdparm setserial smartmontools software-properties-common sphinx-common streamripper \
	subversion texi2html texinfo unclutter unzip uchardet youtube-dl w3m vsftpd xmlto xterm ubuntu-restricted-extras wavpack \
	"

for p in $REQPKG_ALL; do
	echo -n ">>> Checking \"$p\" : "
	dpkg -s $p >/dev/null
	if [[ "$?" -eq "0" ]]; then
		echo "package is installed, skip it"
	else
		echo "package NOT present, installing it"
		apt-get -y install $p
	fi
done

if [[ "$release" = "22.04" ]]; then
	dpkg-reconfigure python3
	echo ""
	echo "************************************************************************************"
	echo "                             *** release 22.04 ***"
	echo "************************************************************************************"
	echo ""
	REQPKG="flake8 gcc-11 g++-11 libssl3 libdca-dev libsdl2-dev libtool-bin libpng-dev libqt5gstreamer-dev libva-glx2 libva-dev liba52-0.7.4-dev libffi7 libfuture-perl ntpsec \
	pycodestyle sqlite3 sphinx-rtd-theme-common libupnp-dev libvdpau1 libvdpau-va-gl1 swig swig3.0 streamlink yamllint ntpsec-ntpdate neurodebian-popularity-contest popularity-contest pylint \
	python3-transmissionrpc python3-sabyenc python3-flickrapi python3-demjson python3-mechanize python3-sendfile python3-blessings python3-httpretty python3-mutagen python3-urllib3 \
	python3-pymysql python3-sphinxcontrib.websupport python3-sphinxcontrib.httpdomain python3-langdetect python3-restructuredtext-lint python3-ntplib python3-ntp python3-pysnmp4 python3-asn1crypto \
	python3-attr python3-autobahn python3-biplist python3-cheroot python3-cheetah python3-cherrypy3 python3-circuits python3-cssselect python3-dnspython python3-feedparser python3-fuzzywuzzy \
	python3-guessit python3-icalendar python3-isodate python3-ndg-httpsclient python3-notify2 python3-pbkdf2 python3-puremagic python3-pycountry python3-setuptools-scm-git-archive python3-pytest \
	python3-singledispatch python3-sphinx-rtd-theme python3-streamlink python3-levenshtein python3-sgmllib3k python3-ujson python3-willow python3-num2words python3-pprintpp  \
	"

	# Unfortunately e2pc doesn't work with wayland
	#	cp -fv /etc/gdm3/custom.conf /etc/gdm3/custom.conf~
	#	rpl '#WaylandEnable=false' 'WaylandEnable=false' /etc/gdm3/custom.conf
fi

for p in $REQPKG; do
	echo -n ">>> Checking \"$p\" : "
	dpkg -s $p >/dev/null
	if [[ "$?" -eq "0" ]]; then
		echo "package is installed, skip it"
	else
		echo "package NOT present, installing it"
		apt-get -y install $p
	fi
done

HEADERS="/usr/src/linux-headers-`uname -r`/include/uapi/linux/dvb"
INCLUDE="/usr/include/linux/dvb"
BUILD_DIR="libs"

cp -fv pre/dvb/* $INCLUDE
cp -fv pre/dvb/* $HEADERS

# Download dvb-firmwares
wget --no-check-certificate https://github.com/crazycat69/media_build/releases/download/latest/dvb-firmwares.tar.bz2
tar -xvjf dvb-firmwares.tar.bz2 -C /lib/firmware
rm -f dvb-firmwares.tar.bz2

if [ -d $BUILD_DIR ]; then
	rm -rf $BUILD_DIR
fi
mkdir -v $BUILD_DIR
cd $BUILD_DIR

# Build and install libdvbsi++-git:
LB="libdvbsi++1"
PKG="libdvbsi++"
#PKG="libdvbsi-"
echo ""
echo "                    *** Build and install $PKG ***"
echo ""
dpkg -s $PKG-dev | grep -iw ok > /dev/null
if [ $? -eq 0 ]; then
	dpkg -r $LB $LB-dbgsym $PKG-dev
else
	echo "$PKG not installed"
fi
if [ -d $PKG ]; then
	rm -rf $PKG
fi
#git clone https://github.com/OpenDMM/$PKG.git
git clone --depth 1 git://git.opendreambox.org/git/obi/$PKG.git
cd $PKG
#autoupdate
dpkg-buildpackage -b -d -uc -us
cd ..
mv $PKG*.* $PKG
cd $PKG
dpkg -i *deb
rm -f *.tar.xz
make distclean
cd ..

# Build and install libxmlccwrap-git:
if [ ! -d libdvbsi++ ]; then
	set -e
	set -o pipefail
else
	PKG="libxmlccwrap"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                     *** Build and install $PKG ***"
	echo ""
	dpkg -s $PKG | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $PKG $PKG-dev $PKG-dbgsym
	else
		echo "$PKG not installed"
	fi
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	git clone https://github.com/OpenDMM/$PKG.git
#	git clone git://git.opendreambox.org/git/obi/$PKG.git
	cd $PKG
	rpl '5' '10' debian/compat
	rpl 'Source-Version' 'binary:Version' debian/control
	sed -i 's/-$(MAKE) clean//g' debian/rules
	sed -i 's/-$(MAKE) distclean//g' debian/rules
#	autoupdate
	dpkg-buildpackage -b -d -uc -us
	cd ..
	mv $PKG*.* $PKG
	cd $PKG
	dpkg -i *deb
	rm -f *.tar.gz
	make distclean
	cd ..
fi

# Build and install libdvbcsa-git:
if [ ! -d libxmlccwrap ]; then
	set -e
	set -o pipefail
else
	PKG="libdvbcsa"
	PKG1="libdvbcsa1"
	VER="bc6c0b164a87ce05e9925785cc6fb3f54c02b026"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                       *** Build and install $PKG ***"
	echo ""
	dpkg -s $PKG | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $PKG $PKG-dev $PKG1 tsdecrypt
	else
		echo "$PKG not installed"
	fi
	dpkg -s $PKG1 | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $PKG1 $PKG-dev tsdecrypt
	else
		echo "$PKG not installed"
	fi
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://code.videolan.org/videolan/$PKG/-/archive/$VER/$PKG-$VER.zip
	unzip $PKG-$VER.zip
	rm $PKG-$VER.zip
	mv $PKG-$VER $PKG
	cd $PKG
	./bootstrap
	./configure --prefix=/usr --enable-sse2
	checkinstall -D --install=yes --default --pkgname=$PKG --pkgversion=1.2.0 --maintainer=e2pc@gmail.com --pkggroup=video --gzman=yes
	rm -f *.tgz
	make distclean
	cd ..
fi

# Build and install libtuxtxt:
if [ ! -d libdvbcsa ]; then
	set -e
	set -o pipefail
else
	INSTALL_E2DIR="/usr/local/e2"
	SOURCE="tuxtxt-git"
	PKG="libtuxtxt"
	PKG_="tuxtxt"
	VER="1402795d660955757d87967b8ff1e3790625f9c1"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                       *** Build and install $PKG ***"
	echo ""
	dpkg -s $PKG | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $PKG
	else
		echo "$PKG not installed"
	fi
	if [ ! -d $INSTALL_E2DIR ]; then
		mkdir -p $INSTALL_E2DIR/lib/enigma2
	fi
	if [ -d $SOURCE ]; then
		dpkg -r $PKG $PKG_
		rm -rf $SOURCE
	fi
	if [ ! -d $INSTALL_E2DIR/lib/enigma2 ]; then
		mkdir -p $INSTALL_E2DIR/lib/enigma2
		ln -s $INSTALL_E2DIR/lib/enigma2 /usr/lib
	fi
	if [ -d $SOURCE ]; then
		rm -rf $SOURCE
	fi
	wget --no-check-certificate https://github.com/OpenPLi/$PKG_/archive/$VER.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG_-$VER $SOURCE
	cd ..
	cp -v patches/$PKG_.patch libs/$SOURCE
	cd libs/$SOURCE
	patch -p1 < $PKG_.patch
	echo ""
	echo "                       *** patches for $PKG applied ***"
	echo ""
	cd $PKG
#	autoupdate
	autoreconf -i
	./configure --prefix=/usr --with-boxtype=generic DVB_API_VERSION=5
	checkinstall -D --install=yes --default --pkgname=$PKG --pkgversion=1.0 --maintainer=e2pc@gmail.com --pkggroup=video --gzman=yes
	rm -f *.tgz
	make distclean
	cd ..
fi

# Build and install tuxtxt:
if [ ! -d libtuxtxt ]; then
	set -e
	set -o pipefail
else
	PKG="tuxtxt"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                        *** Build and install $PKG ***"
	echo ""
	dpkg -s $PKG | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $PKG
	else
		echo "$PKG not installed"
	fi
	cd $PKG
#	autoupdate
	autoreconf -i
	./configure --prefix=/usr --with-boxtype=generic --with-configdir=/usr/etc --with-fbdev=/dev/fb0 --with-textlcd DVB_API_VERSION=5
	checkinstall -D --install=yes --default --pkgname=$PKG --pkgversion=1.0 --maintainer=e2pc@gmail.com --pkggroup=video --gzman=yes
	find $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/Tuxtxt -name "*.py[o]" -exec rm {} \;
	rm -f *.tgz
	make distclean
	cd ../..
fi

# Build and install aio-grab-git:
if [ ! -d tuxtxt-git/tuxtxt ]; then
	set -e
	set -o pipefail
else
	PKG="aio-grab"
	VER="cf62da47eedb6afe4c44949253ef0b876deb2105"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                       *** Build and install $PKG ***"
	echo ""
	dpkg -s $PKG | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $PKG
	else
		echo "$PKG not installed"
	fi
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/OpenPLi/$PKG/archive/$VER.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG-$VER $PKG
	cd $PKG
	autoreconf -i
	./configure --prefix=/usr
	checkinstall -D --install=yes --default --pkgname=$PKG --pkgversion=1.0 --maintainer=e2pc@gmail.com --pkggroup=video --gzman=yes
	rm -f *.tgz
	make distclean
	cd ..
fi

# Build and install gst-plugin-dvbmediasink-git:
if [ ! -d aio-grab ]; then
	set -e
	set -o pipefail
else
	LB="libgstreamer-plugins-dvbmediasink"
	PKG="gst-plugin-dvbmediasink"
	VER="1d197313832d39fdaf430634f62ad95a33029db0"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                 *** Build and install $PKG ***"
	echo ""
	dpkg -s $LB | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $LB
	else
		echo "$LB not installed"
	fi
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/OpenPLi/$PKG/archive/$VER.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG-$VER $PKG
	cd $PKG
#	autoupdate
	autoreconf -i
	./configure --prefix=/usr --with-wma --with-wmv --with-pcm --with-dtsdownmix --with-eac3 --with-mpeg4 --with-mpeg4v2 --with-h263 --with-h264 --with-h265
	checkinstall -D --install=yes --default --pkgname=$LB --pkgversion=1.0.0 --maintainer=e2pc@gmail.com --pkggroup=video --gzman=yes
	rm -f *.tgz
	make distclean
	cd ..
fi

# Build and install gst-plugin-subsink-git:
if [ ! -d gst-plugin-dvbmediasink ]; then
	set -e
	set -o pipefail
else
	LB="libgstreamer-plugins-subsink"
	PKG="gst-plugin-subsink"
	VER="2c4288bb29e0781f27aecc25c941b6e441630f8d"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	dpkg -s $LB | grep -iw ok > /dev/null
	if [ $? -eq 0 ]; then
		dpkg -r $LB
	else
		echo "$LB not installed"
	fi
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/OpenPLi/$PKG/archive/$VER.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG-$VER $PKG
	cd ..
	cp -v patches/subsink_1.0.patch libs/$PKG
	cd libs/$PKG
	echo "AC_CONFIG_MACRO_DIR([m4])" >> configure.ac
	patch -p1 < subsink_1.0.patch
	echo ""
	echo "                  *** Patch for $PKG applied ***"
	echo ""
	#autoupdate
	autoreconf -i
	./configure --prefix=/usr
	checkinstall -D --install=yes --default --pkgname=$LB --pkgversion=1.0 --maintainer=e2pc@gmail.com --pkggroup=video --gzman=yes
	rm -f *.tgz
	make distclean
	cd ..
fi

# Build and install twistedsnmp-python3:
if [ ! -d gst-plugin-subsink ]; then
	set -e
	set -o pipefail
else
	PKG="twistedsnmp"
	VER="caab5fb520ee8f1535a1500324a0254df268d0ba"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/mcfletch/twistedsnmp/archive/caab5fb520ee8f1535a1500324a0254df268d0ba.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG-$VER $PKG
	cd ..
	cp -v patches/$PKG-python3.patch libs/$PKG
	cd libs/$PKG
	patch -p1 < $PKG-python3.patch
	echo ""
	echo "                  *** Patch for $PKG applied ***"
	echo ""
	python3 setup.py install
	cd ..
fi

# Build and install python3-pythonwifi:
if [ ! -d twistedsnmp ]; then
	set -e
	set -o pipefail
else
	PKG="pythonwifi"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/athoik/pythonwifi/archive/refs/heads/master.zip
	unzip master.zip
	rm -f master.zip
	mv $PKG-master $PKG
	cd $PKG
	python3 setup.py install
	cd ..
fi

# Build and install python3-Js2Py:
if [ ! -d pythonwifi ]; then
	set -e
	set -o pipefail
else
	PKG="Js2Py"
	VER="b16d7ce90ac9c03358010c1599c3e87698c9993f"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/PiotrDabkowski/Js2Py/archive/$VER.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG-$VER $PKG
	cd ..
	cp patches/$PKG.patch libs/$PKG
	cd libs/$PKG
	patch -p1 < $PKG.patch
	python3 setup.py install
	cd ..
fi

# Build and install python3-ipaddress:
if [ ! -d Js2Py ]; then
	set -e
	set -o pipefail
else
	PKG="ipaddress"
	VER="d8aef06cc3ca8a6fd8570cda665b2bb879a29390"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/phihag/ipaddress/archive/$VER.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG-$VER $PKG
	cd ..
	cp patches/$PKG.patch libs/$PKG
	cd libs/$PKG
	patch -p1 < $PKG.patch
	python3 setup.py install
	cd ..
fi

# Build and install PythonDaap:
if [ ! -d ipaddress ]; then
	set -e
	set -o pipefail
else
	PKG="PythonDaap"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/abdelgmartinezl/PythonDaap/archive/refs/heads/master.zip
	unzip master.zip
	rm -f master.zip
	mv $PKG-master $PKG
	cd ..
	cp patches/$PKG.patch libs/$PKG
	cd libs/$PKG
	patch -p1 < $PKG.patch
	python3 setup.py install
	cd ..
fi

# Build and install python3-pyload:
if [ ! -d PythonDaap ]; then
	set -e
	set -o pipefail
else
	PKG="pyload"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/pyload/pyload/archive/refs/heads/main.zip
	unzip main.zip
	rm main.zip
	mv $PKG-main $PKG
	cd ..
	cp patches/$PKG.patch libs/$PKG
	cd libs/$PKG
	patch -p1 < $PKG.patch
	python3 setup.py install
	cd ..
fi

# Build and install python3-livestreamersrv:
if [ ! -d pyload ]; then
	set -e
	set -o pipefail
else
	PKG="livestreamersrv"
	VER="d8c0258b178a42c76fadfbddb9ac773646d2557e"
	echo ""
	echo "**************************** OK. Go to the next step. ******************************"
	echo ""
	echo "                    *** Build and install $PKG ***"
	echo ""
	if [ -d $PKG ]; then
		rm -rf $PKG
	fi
	wget --no-check-certificate https://github.com/oe-mirrors/livestreamersrv/archive/$VER.zip
	unzip $VER.zip
	rm $VER.zip
	mv $PKG-$VER $PKG
	# Place for cp?
fi

# Message if error at any point of script
if [ ! -d livestreamersrv ]; then
	set -e
	set -o pipefail
	echo ""
	echo "          *** Forced stop script execution. It maybe сompilation error, ***"
	echo "           *** lost Internet connection or the server not responding. ***"
	echo "                    *** Check the log for more information. ***"
	echo ""
else
	cd ..
	if [ ! -f /usr/lib/python3/dist-packages/fix-writing-after-channel-is-closed.patch ]; then
		cp patches/fix-writing-after-channel-is-closed.patch /usr/lib/python3/dist-packages
		cd /usr/lib/python3/dist-packages
		patch -p1 < fix-writing-after-channel-is-closed.patch
	else
		echo ""
		echo "************************ The file http.py already patched. *************************"
		echo ""
	fi
	cd ..
	pip install pysmb zope.interface pycryptodomex pysocks rbtranslations soco tenjin tcpbridge pyserial PyHamcrest \
	pyexecjs py3amf pillow gdata-python3 futures3 cocy circuits-bricks cfscrape bluetool pyopenssl pyusb
	pip install -U pyopenssl
	python3 -m pip install pysha3
	echo ""
	echo "************************************ DONE! *****************************************"
fi
