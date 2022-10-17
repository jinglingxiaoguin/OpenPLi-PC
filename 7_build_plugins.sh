#!/bin/bash

# Build and install plugins for enigma2pc

release=$(lsb_release -a 2>/dev/null | grep -i release | awk ' { print $2 } ')
INSTALL_E2DIR="/usr/local/e2"
P3_PACKAGES="/usr/local/lib/python3.10/dist-packages"
MAKE_J="9"

if [ "$release" = "22.04" ]; then

	# Removing old compiled pyc files
	find $INSTALL_E2DIR/lib/enigma2/python/ -name "*.py[c]" -exec rm {} \;

	if [ -d plugins ]; then # This is the lock from the unpredictable script actions in the root directory in the absence of the plugins folder.
		cd plugins/enigma2-plugins
		echo ""
		echo "************************************************************************************"
		echo "                             *** release 22.04 ***"
		echo "                              *** used g++-11 ***"
		echo "************************************************************************************"
		echo ""
		cd ../..
		cp -fv pre/include/rpc/* /usr/include/rpc
		cd plugins/enigma2-plugins

		export CXX=/usr/bin/g++-11
		export PYTHON_VERSION=3.10
		export PYTHON_CPPFLAGS=-I/usr/include/python3.10
		export PYTHON_LDFLAGS="-L/usr/lib/python3.10 -lpython3.10"
		export PYTHON_EXTRA_LIBS="-lpthread -ldl -lutil -lm"
		export PYTHON_EXTRA_LDFLAGS="-Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions"

		# Build enigma2 cpp plugins:
		echo ""
		echo "************************** OK. Let's build the plugins. ****************************"
		echo ""
		PKG="servicemp3"
		VER="a6b2178d0ebe5831aca5e8ba8d2da0f790e7b63a"
		if [ -d $PKG ]; then
			rm -rf $PKG
		fi
		wget https://github.com/OpenPLi/$PKG/archive/$VER.zip
		unzip $VER.zip
		rm $VER.zip
		mv $PKG-$VER $PKG
		cd ../..
		cp -fv patches/$PKG.patch plugins/enigma2-plugins/$PKG
		cd plugins/enigma2-plugins/$PKG
		patch -p1 < $PKG.patch
		cd ..
		#autoupdate
		autoreconf -i
		PKG_CONFIG_PATH=$INSTALL_E2DIR/lib/pkgconfig ./configure --prefix=$INSTALL_E2DIR
		make -j"$MAKE_J"
		make install
		cd ..

		if [ ! -d e2openplugin ]; then
			mkdir e2openplugin
		fi

		# Build enigma2-plugin-extensions-ts-sateditor:
		if [ ! -d enigma2-plugins/servicemp3 ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			cd e2openplugin
			PKG="enigma2-plugin-extensions-ts-sateditor"
			PKG_="TSsatEditor"
			VER="7a930d688ccfb540d5213c9df8e337d5c45f5a5b"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/SystemPlugins/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/SystemPlugins/$PKG_
			fi
			wget https://github.com/Dima73/enigma2-plugin-extensions-ts-sateditor/archive/7a930d688ccfb540d5213c9df8e337d5c45f5a5b.zip
			unzip $VER.zip
			rm $VER.zip
			mv $PKG-$VER $PKG
			cd ../..
			cp patches/tssateditor.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < tssateditor.patch
			python3 setup.py install
			mv $P3_PACKAGES/SystemPlugins/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/SystemPlugins
			cd ..
		fi

		# Build e2openplugin-StreamInterface:
		if [ ! -d enigma2-plugin-extensions-ts-sateditor ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-StreamInterface"
			PKG_="StreamInterface"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/refs/heads/python3.zip
			unzip python3.zip
			rm python3.zip
			mv $PKG-python3 $PKG
			cd $PKG
			python3 setup.py install && python3 setup.py install # It's right
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build e2openplugin-SystemTools
		if [ ! -d e2openplugin-StreamInterface ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-SystemTools"
			PKG_="SystemTools"
			VER="88dbcac49202a4d850221841b8f16891f684a375"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/$VER.zip
			unzip $VER.zip
			rm $VER.zip
			mv $PKG-$VER $PKG
			cd ../..
			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG_.patch
			python3 setup.py install && python3 setup.py install # It's right
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build e2openplugin-AddStreamUrl
		if [ ! -d e2openplugin-SystemTools ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-AddStreamUrl"
			PKG_="AddStreamUrl"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/refs/heads/python3.zip
			unzip python3.zip
			rm python3.zip
			mv $PKG-python3 $PKG
			cd ../..
			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG_.patch
			python3 setup.py install && python3 setup.py install # It's right
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build e2openplugin-OpenWebif
		if [ ! -d e2openplugin-AddStreamUrl ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-OpenWebif"
			PKG_="OpenWebif"
			VER="50e162b3fbfc85052968b4aaf52fc9bcca6d426a"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/$VER.zip
			unzip $VER.zip
			rm $VER.zip
			mv $PKG-$VER $PKG
			cd ../..
			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG_.patch
			mv CI/create_ipk.sh create_ipk.sh
			./create_ipk.sh
			ar -x *.ipk
			tar -xvf data.tar.gz
			mv usr/lib/enigma2/python/Plugins/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions # It's right
			rm -rf debian-binary usr *.gz *.ipk
			cd ..
		fi

		# Build e2openplugin-SetPicon
		if [ ! -d e2openplugin-OpenWebif ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-SetPicon"
			PKG_="SetPicon"
			VER="6b777ed10fba7a825ba99ca8a27f6c381dee6d16"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/$VER.zip
			unzip $VER.zip
			rm $VER.zip
			mv $PKG-$VER $PKG
			cd ../..
			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG_.patch
			python3 setup.py install && python3 setup.py install # It's right
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build e2openplugin-SnmpAgent
#		if [ ! -d e2openplugin-SetPicon ]; then
#			set -e
#			set -o pipefail
#		else
#			echo ""
#			echo "**************************** OK. Go to the next step. ******************************"
#			echo ""
#			PKG="e2openplugin-SnmpAgent"
#			PKG_="SnmpAgent"
#			VER="450ed959a78918a08a3df5a58acb99d2bdc90f5b"
#			if [ -d $PKG ]; then
#				rm -rf $PKG
#			fi
#			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
#				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
#			fi
#			wget https://github.com/E2OpenPlugins/$PKG/archive/$VER.zip
#			unzip $VER.zip
#			rm $VER.zip
#			mv $PKG-$VER $PKG
#			cd ../..
#			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
#			cd plugins/e2openplugin/$PKG
#			patch -p1 < $PKG_.patch
#			python3 setup.py install
#			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
#			cd ..
#		fi

		# Build e2openplugin-SimpleUmount
#		if [ ! -d e2openplugin-SnmpAgent ]; then
		if [ ! -d e2openplugin-SetPicon ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-SimpleUmount"
			PKG_="SimpleUmount"
			VER="c8517274748ebe7789b03cfcb4ff142332e7ea02"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/$VER.zip
			unzip $VER.zip
			rm $VER.zip
			mv $PKG-$VER $PKG
			cd ../..
			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG_.patch
			python3 setup.py install && python3 setup.py install # It's right
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build e2openplugin-Foreca
		if [ ! -d e2openplugin-SimpleUmount ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-Foreca"
			PKG_="Foreca"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/refs/heads/python3.zip
			unzip python3.zip
			rm python3.zip
			mv $PKG-python3 $PKG
			cd ../..
			cp patches/$PKG_.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG_.patch
			python3 setup.py install && python3 setup.py install # It's right
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build enigma2-plugin-youtube
		if [ ! -d e2openplugin-Foreca ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="enigma2-plugin-youtube"
			PKG_="YouTube"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/Taapat/$PKG/archive/refs/heads/master.zip
			unzip master.zip
			rm master.zip
			mv $PKG-master $PKG
			cd $PKG
			python3 setup.py install
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build e2openplugin-OscamStatus
		if [ ! -d enigma2-plugin-youtube ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2openplugin-OscamStatus"
			PKG_="OscamStatus"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			wget https://github.com/E2OpenPlugins/$PKG/archive/refs/heads/master.zip
			unzip master.zip
			rm master.zip
			mv $PKG-master $PKG
			cd ../..
			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG_.patch
			python3 setup.py install
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cd ..
		fi

		# Build enigma2-plugin-extensions-epgimport
#		if [ ! -d e2openplugin-OscamStatus ]; then
#			set -e
#			set -o pipefail
#		else
#			echo ""
#			echo "**************************** OK. Go to the next step. ******************************"
#			echo ""
#			PKG="enigma2-plugin-extensions-epgimport"
#			PKG_="EPGImport"
#			VER="a82a48233dad402a7e5ed69edfa2720a793f3dcd"
#			if [ -d $PKG ]; then
#				rm -rf $PKG
#			fi
#			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
#				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
#			fi
#			wget https://github.com/OpenPLi/$PKG/archive/$VER.zip
#			unzip $VER.zip
#			rm $VER.zip
#			mv $PKG-$VER $PKG
#			cd ../..
#			cp -fv patches/$PKG_.patch plugins/e2openplugin/$PKG
#			cd plugins/e2openplugin/$PKG
#			patch -p1 < $PKG_.patch
#			cd src
#			python3 setup.py install
#			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
#			cd ../..
#		fi

		# Build enigma2-plugin-mountmanager
		if [ ! -d e2openplugin-OscamStatus ]; then
			set -e
			set -o pipefail
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="enigma2-plugin-mountmanager"
			PKG_="MountManager"
			VER="63646c2e38ae187aa69fe3be3d8b94e3c479541b"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/SystemPlugins/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/SystemPlugins/$PKG_
			fi
			wget https://github.com/Dima73/$PKG/archive/$VER.zip
			unzip $VER.zip
			rm $VER.zip
			mv $PKG-$VER $PKG
			cd $PKG
			python3 setup.py install
			mv $P3_PACKAGES/SystemPlugins/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/SystemPlugins
			cd ..
		fi

		# Build e2iplayer
		if [ ! -d enigma2-plugin-mountmanager ]; then
			set -e
			set -o pipefail
			# Message if error at any point of script
			echo ""
			echo "************ Forced stop script execution. It maybe сompilation error, *************"
			echo "************** lost Internet connection or the server not responding. **************"
			echo "*********************** Check the log for more information. ************************"
			echo ""
		else
			echo ""
			echo "**************************** OK. Go to the next step. ******************************"
			echo ""
			PKG="e2iplayer"
			PKG_="IPTVPlayer"
			PKG__="E2IPlayer"
			VER="aeaa0ad88c9cc4d01c13057d57b2764bf580a7b5"
			if [ -d $PKG ]; then
				rm -rf $PKG
			fi
			if [ -d $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_ ]; then
				rm -rf $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			fi
			rm -f /usr/lib/librtmp.so.1
			wget https://gitlab.com/zadmario/e2iplayer/-/archive/$VER/e2iplayer-$VER.zip
			unzip $PKG-$VER.zip
			rm $PKG-$VER.zip
			mv $PKG-$VER $PKG
			cd ../..
			cp -rv pre/icons plugins/e2openplugin/$PKG/$PKG_
			cp -fv patches/$PKG__.patch plugins/e2openplugin/$PKG
			cd plugins/e2openplugin/$PKG
			patch -p1 < $PKG__.patch
			rm -f IPTVPlayer/locale/ru/LC_MESSAGES/.gitkeep
			python3 setup.py install
			mv $P3_PACKAGES/Extensions/$PKG_ $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions
			cp -rfv IPTVPlayer/locale $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_
			wget http://iptvplayer.vline.pl/resources/bin/i686/_subparser.so
			chmod 755 _subparser.so
			mv _subparser.so $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/libs/iptvsubparser
			wget http://iptvplayer.vline.pl/resources/bin/i686/duk
			chmod 755 duk
			mv duk $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/bin
			rm -f /usr/bin/duk
			wget http://iptvplayer.vline.pl/resources/bin/i686/hlsdl_static_curl_openssl.1.0.2
			chmod 755 hlsdl_static_curl_openssl.1.0.2
			mv hlsdl_static_curl_openssl.1.0.2 $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/bin/hlsdl
			rm -f /usr/bin/hlsdl
			wget http://iptvplayer.vline.pl/resources/bin/i686/f4mdump_openssl.1.0.2
			chmod 755 f4mdump_openssl.1.0.2
			mv f4mdump_openssl.1.0.2 $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/bin/f4mdump
			rm -f /usr/bin/f4mdump
			wget http://iptvplayer.vline.pl/resources/bin/i686/uchardet
			chmod 755 uchardet
			mv uchardet $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/bin
			wget http://iptvplayer.vline.pl/resources/bin/i686/wget_openssl.1.0.2
			chmod 755 wget_openssl.1.0.2
			mv wget_openssl.1.0.2 $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/bin/fullwget
			cd ..
			if [ -d e2iplayer ]; then
				wget http://iptvplayer.vline.pl/resources/bin/i686/gstplayer_gstreamer1.0
				mv gstplayer_gstreamer1.0 gstplayer
				chmod 755 gstplayer
				mv gstplayer $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/bin
				rm -f /usr/bin/gstplayer
			fi
			if grep "config.plugins.iptvplayer.wgetpath=/usr/bin/wget" $INSTALL_E2DIR/etc/enigma2/settings; then
				echo ""
				echo ""
				echo "*************************** Detected $PKG_ settings.***************************"
			else
				echo ""
				echo "******************* There are no iptvplayer settings. Adding...*********************"
				echo "config.plugins.iptvplayer.autoCheckForUpdate=false" >> $INSTALL_E2DIR/etc/enigma2/settings
				echo "config.plugins.iptvplayer.deleteIcons=0" >> $INSTALL_E2DIR/etc/enigma2/settings
				echo "config.plugins.iptvplayer.downgradePossible=true" >> $INSTALL_E2DIR/etc/enigma2/settings
				echo "config.plugins.iptvplayer.dukpath=$INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/$PKG_/bin/duk" >> $INSTALL_E2DIR/etc/enigma2/settings
				echo "config.plugins.iptvplayer.possibleUpdateType=sourcecode" >> $INSTALL_E2DIR/etc/enigma2/settings
				echo "config.plugins.iptvplayer.showinMainMenu=true" >> $INSTALL_E2DIR/etc/enigma2/settings
				echo "config.plugins.iptvplayer.uchardetpath=/usr/bin/uchardet" >> $INSTALL_E2DIR/etc/enigma2/settings
				echo "config.plugins.iptvplayer.wgetpath=/usr/bin/wget" >> $INSTALL_E2DIR/etc/enigma2/settings
			fi
		fi

		cd ../..

		# For use *.m3u8 in the /tmp folder
		chown $(who | gawk '{print $1}'):$(who | gawk '{print $1}') /tmp

		# Copy files to $INSTALL_E2DIR
		echo ""
		echo "******************************** Copy  plugins E2PC ********************************"
		cp -rfv plugins/third-party-plugins/* $INSTALL_E2DIR/lib/enigma2/python
		cp -rfv pre/epgimport $INSTALL_E2DIR/etc
		cp -rfv pre/xmltvimport $INSTALL_E2DIR/etc
		cp -rfv skins/* $INSTALL_E2DIR

		if [ ! -f /usr/local/bin/bitrate ]; then
			ln -sf $INSTALL_E2DIR/bin/bitrate /usr/local/bin
		fi

		# Create folder for softam keys and symlink for plugin 'navibar'
		if [ ! -d /var/keys ]; then
			mkdir -p /var/keys
		fi
#		if [ ! -d /home/hdd/icons ]; then
#			ln -s $INSTALL_E2DIR/lib/enigma2/python/Plugins/Extensions/navibar/icons /home/hdd
#		fi

		# Force compile pyc files
		#python3 -m compileall -f $INSTALL_E2DIR/lib/enigma2/python

		echo ""
		echo "************* Plugins, skins, E2PC python files installed successfully.*************"
	else
		echo ""
		echo "************ Plugins folder is missing! Please run scripts step by step! ************"
	fi # End lock
else
	echo ""
	echo "********************  Sorry but this is for Ubuntu 22.04 only! **********************"
fi
