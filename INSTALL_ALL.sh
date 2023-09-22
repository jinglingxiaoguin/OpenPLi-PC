#!/bin/sh

#./0_optional_media_build.sh
./1_build_e2_procfs.sh
./2_build_libs.sh
./3_build_libsigc_3.0.sh
#./4_optional_partial_environment_22.04.sh
./5_build_libxine.sh
./6_build_openpliPC.sh
./7_build_plugins.sh
./8_build_oscam.sh
./9_build_lirc.sh
