#!/bin/bash

release=$(lsb_release -a 2>/dev/null | grep -i release | awk ' { print $2 } ')

if [[ "$release" = "23.04" ]]; then
	mkdir driver
	cd driver
	wget http://archive.ubuntu.com/ubuntu/pool/universe/i/intel-vaapi-driver/i965-va-driver_2.4.1+dfsg1-1_amd64.deb
	wget http://archive.ubuntu.com/ubuntu/pool/universe/i/intel-media-driver/intel-media-va-driver_22.3.1+dfsg1-1ubuntu2_amd64.deb
	wget http://archive.ubuntu.com/ubuntu/pool/universe/libv/libva/va-driver-all_2.14.0-1_amd64.deb
	dpkg -i *deb
	cd ..
	mkdir libva
	cd libva
	wget http://archive.ubuntu.com/ubuntu/pool/universe/libv/libva/libva2_2.14.0-1_amd64.deb
	wget http://archive.ubuntu.com/ubuntu/pool/universe/libv/libva/libva-dev_2.14.0-1_amd64.deb
	wget http://archive.ubuntu.com/ubuntu/pool/universe/libv/libva/libva-drm2_2.14.0-1_amd64.deb
	wget http://archive.ubuntu.com/ubuntu/pool/universe/libv/libva/libva-glx2_2.14.0-1_amd64.deb
	wget http://archive.ubuntu.com/ubuntu/pool/universe/libv/libva/libva-wayland2_2.14.0-1_amd64.deb
	wget http://archive.ubuntu.com/ubuntu/pool/universe/libv/libva/libva-x11-2_2.14.0-1_amd64.deb
	dpkg -i *deb
	cd ..
fi
