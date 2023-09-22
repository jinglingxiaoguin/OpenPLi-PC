#!/bin/sh

release=$(lsb_release -a 2>/dev/null | grep -i release | awk ' { print $2 } ')

if [[ "$release" = "22.04" ]]; then
	PKG="libsigc--3.0"
	REQPKG="mm-common"

	echo ""
	echo "                       *** INSTALL REQUIRED PACKAGES ***"
	echo ""

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

	cd libs

	if [ -d $PKG ]; then
		rm -vfR $PKG
	fi

	git clone https://github.com/dbus-cxx/$PKG.git
	cd $PKG
	./autogen.sh --prefix=/usr

	make -j3
	make install
else
	echo ""
	echo "                       *** Not need for Ubuntu 23.04 ***"
	echo ""
fi
