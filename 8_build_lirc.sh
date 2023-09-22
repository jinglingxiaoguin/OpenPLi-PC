
# Script for install patched lirc-0.10.1-7.2-e2pc on Ubuntu-22.04 only.

# If your system has two devices /dev/lirc0 and /dev/lirc1 (for example, a built-in IR-receiver in the card card)
# then you can add a rule to /etc/udev/rules.d/99-lirc-symlinks.rules:
# KERNELS=="serial_ir.0", SUBSYSTEM=="lirc", DRIVERS=="serial_ir", ATTRS{driver_override}=="(null)", SYMLINK+="lirc_serial"
# and use "/dev/lirc_serial" in your *.lircd.conf.
# You also need to disable the uinput service by command:
# systemctl mask lircd-uinput.service
# and then reboot the system.

release=$(lsb_release -a 2>/dev/null | grep -i release | awk ' { print $2 } ')

PKG="lirc-0.10.1"
DIR="lirc_build"
CONF="/etc/lirc"
DH="dh-systemd_12.1.1~nd20.04+1_all.deb"
P1="lirc-python3.10.patch"
P2="lirc-python3.11.patch"

apt install -y dh-exec dh-python doxygen expect libftdi1-dev libsystemd-dev libudev-dev libusb-dev man2html-base portaudio19-dev python3-dev python3-setuptools python3-xyzservices socat setserial xsltproc
pip install --upgrade websockets
pip uninstall PyCrypto
pip install -U PyCryptodome
wget https://neurodebian.g-node.org/pool/main/d/debhelper/$DH
dpkg -i $DH
rm -f $DH
if [ -d $DIR ]; then
	rm -fr $DIR
fi
mkdir $DIR
cd $DIR
wget https://launchpadlibrarian.net/643046456/lirc_0.10.1.orig.tar.gz
tar -xvf lirc_0.10.1.orig.tar.gz
rm -f lirc_0.10.1.orig.tar.gz
cd ..

if [[ "$release" = "22.04" ]]; then
	cp -v patches/$P1 $DIR/$PKG
	cd $DIR/$PKG
	patch -p1 < $P1
fi
if [[ "$release" = "23.04" ]]; then
	cp -v patches/$P2 $DIR/$PKG
	cd $DIR/$PKG
	patch -p1 < $P2
fi

rm -f *.patch
chmod 755 debian/install
chmod 755 debian/pbuilder-test
chmod 755 debian/lirc-old2new
chmod 755 debian/postrm
cd ..
tar -cvzf lirc_0.10.1.orig.tar.gz $PKG
cd $PKG
dpkg-buildpackage -b -d -uc -us
cd ..
yes | dpkg -i *.deb
cd ..
cp -rfv pre/lirc/lircd.conf.d /etc
cp -rfv pre/lirc/lirc_options.conf.example /etc
mv /etc/lirc/lirc_options.conf.example lirc_options.conf
cp -fv pre/99-lirc-symlinks.rules /etc/udev/rules.d
if [ -f $CONF/lircd.conf.d/devinput.lircd.conf ]; then
	mv -b $CONF/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.conf.dist
fi
if [ -f $CONF/irexec.lircrc ]; then
	mv -b $CONF/irexec.lircrc $CONF/irexec.lircrc.dist
fi
if [ -f $CONF/irexec.lircrc ];then
	rm -f $CONF/irexec.lircrc
fi

systemctl enable lircd.socket
systemctl start lircd.socket
systemctl enable lircmd.service
systemctl start lircmd.service
systemctl mask lircd-uinput.service
systemctl daemon-reload
systemctl start lircd
systemctl restart lircd

echo ""
echo "NOW THE SYSTEM WILL BE RESTARTED!"
echo ""

sleep 5
reboot # Need to restart system!
