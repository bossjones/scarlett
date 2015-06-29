#!/bin/bash

# install base python shit
# install

export GSTREAMER=1.0
export MAIN_DIR=~/dev/scarlett
export VIRT_ROOT=/home/pi/.virtualenvs/scarlett-travis
export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig
export SCARLETT_CONFIG=$MAIN_DIR/tests/fixtures/.scarlett
export SCARLETT_HMM=$MAIN_DIR/tests/fixtures/model/hmm/en_US/hub4wsj_sc_8k
export SCARLETT_LM=$MAIN_DIR/tests/fixtures/lm/1602.lm
export SCARLETT_DICT=$MAIN_DIR/tests/fixtures/dict/1602.dic

sudo apt-get install git -y
git clone https://github.com/bossjones/scarlett --branch feature-new-gst ~/dev/scarlett

sudo apt-get update -qq
sudo apt-get install -yqq build-essential libssl-dev libreadline-dev wget

# install python
sudo apt-get -yqq install python python-pip python-dev && sudo easy_install --upgrade pip && sudo easy_install --upgrade setuptools

pip install virtualenv virtualenvwrapper
mkvirtualenv scarlett-travis

sudo apt-get install -qq git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev python-numpy python-scipy
sudo add-apt-repository -y ppa:gstreamer-developers/ppa
sudo apt-get update -qq
sudo apt-get install -qq bash-completion swig
pip install tox sphinx nose
sudo apt-get install -qq build-essential autotools-dev automake autoconf libtool autopoint libxml2-dev zlib1g-dev libglib2.0-dev pkg-config bison flex python git gtk-doc-tools libasound2-dev libgudev-1.0-dev libxt-dev libvorbis-dev libcdparanoia-dev libpango1.0-dev libtheora-dev libvisual-0.4-dev iso-codes libgtk-3-dev libraw1394-dev libiec61883-dev libavc1394-dev libv4l-dev libcairo2-dev libcaca-dev libspeex-dev libpng-dev libshout3-dev libjpeg-dev libaa1-dev libflac-dev libdv4-dev libtag1-dev libwavpack-dev libpulse-dev libsoup2.4-dev libbz2-dev libcdaudio-dev libdc1394-22-dev ladspa-sdk libass-dev libcurl4-gnutls-dev libdca-dev libdirac-dev libdvdnav-dev libexempi-dev libexif-dev libfaad-dev libgme-dev libgsm1-dev libiptcdata0-dev libkate-dev libmimic-dev libmms-dev libmodplug-dev libmpcdec-dev libofa0-dev libopus-dev librsvg2-dev librtmp-dev libschroedinger-dev libslv2-dev libsndfile1-dev libsoundtouch-dev libspandsp-dev libx11-dev libxvidcore-dev libzbar-dev libzvbi-dev liba52-0.7.4-dev libcdio-dev libdvdread-dev libmad0-dev libmp3lame-dev libmpeg2-4-dev libopencore-amrnb-dev libopencore-amrwb-dev libsidplay1-dev libtwolame-dev libx264-dev
sudo apt-get install -qq libgirepository1.0-dev gstreamer1.0-plugins-good gir1.2-clutter-1.0 gir1.2-clutter-gst-1.0 gir1.2-gtkclutter-1.0 gir1.2-gtksource-3.0 gir1.2-vte-2.90 gir1.2-webkit-1.0 gir1.2-webkit-3.0
sudo apt-get install -qq git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev libpq-dev libmysqlclient-dev
sudo apt-get install -qq libglib2.0-*
sudo apt-get install -qq git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev libpq-dev libmysqlclient-dev


##### DISABLE # export MAIN_DIR=$(pwd)
##### DISABLE # export VIRT_ROOT=/home/travis/virtualenv/python$TRAVIS_PYTHON_VERSION
##### DISABLE # export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig
##### DISABLE # export SCARLETT_CONFIG=$MAIN_DIR/tests/fixtures/.scarlett
##### DISABLE # export SCARLETT_HMM=$MAIN_DIR/tests/fixtures/model/hmm/en_US/hub4wsj_sc_8k
##### DISABLE # export SCARLETT_LM=$MAIN_DIR/tests/fixtures/lm/1602.lm
##### DISABLE # export SCARLETT_DICT=$MAIN_DIR/tests/fixtures/dict/1602.dic

env | sort
ls -lta $VIRTUAL_ENV/include/
ls -lta $VIRTUAL_ENV/include/*
ls -lta $VIRTUAL_ENV/lib/
ls -lta $VIRTUAL_ENV/lib/*
ls -lta $VIRTUAL_ENV/lib/python2.7/site-packages/
ls -lta $VIRTUAL_ENV/lib/python2.7/site-packages/*

sudo apt-get -qq install git build-essential automake libtool itstool gtk-doc-tools gnome-common gnome-doc-utils yasm flex bison
sudo apt-get -qq install python-gst0.10 python-gst0.10-dev gstreamer0.10-plugins-good
sudo apt-get -qq install gstreamer0.10-ffmpeg gstreamer-tools gstreamer0.10-alsa gstreamer0.10-nice gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly gstreamer0.10-tools libgstreamer-plugins-bad0.10-0 libgstreamer-plugins-bad0.10-dev libgstreamer-plugins-base0.10-0 libgstreamer-plugins-base0.10-dev libgstreamer0.10-0 libgstreamer0.10-0-dbg libgstreamer0.10-cil-dev libgstreamer0.10-dev libgstrtspserver-0.10-0 libgstrtspserver-0.10-dev libnice-dev
sudo apt-get -qq install gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly
sudo apt-get -qq install gstreamer0.10-pulseaudio
sudo apt-get -qq install gstreamer0.10-alsa
sudo apt-get -qq install pavucontrol gstreamer0.10-pulseaudio pulseaudio
sudo apt-get -qq install gstreamer0.10-pulseaudio libao4 libasound2-plugins libgconfmm-2.6-1c2 libglademm-2.4-1c2a libpulse-dev libpulse-mainloop-glib0 libpulse-mainloop-glib0-dbg libpulse0 libpulse0-dbg libsox-fmt-pulse paman paprefs pavucontrol pavumeter pulseaudio pulseaudio-dbg pulseaudio-esound-compat pulseaudio-esound-compat-dbg pulseaudio-module-bluetooth pulseaudio-module-gconf pulseaudio-module-jack pulseaudio-module-lirc pulseaudio-module-lirc-dbg pulseaudio-module-x11 pulseaudio-module-zeroconf pulseaudio-module-zeroconf-dbg pulseaudio-utils
sudo apt-get -qq install bison
sudo apt-get -qq install autoconf automake bison build-essential libasound2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libtool python-gst0.10 python-pyside python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-iplib python-simplejson
sudo apt-get -qq install python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-pip python-setuptools python-gtk2 python-yaml python-yaml-dbg
sudo apt-get -qq install python2.7-dev
sudo apt-get -qq install bison
sudo apt-get -qq install gstreamer1.0* libgstreamer1.0*
sudo apt-get -qq install python-gst* python-pip python-setuptools
sudo apt-get -qq install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get -qq install libusb-1.0
sudo apt-get install yelp-tools -qq
sudo apt-get install python3 python3-dev -qq
sudo apt-get install python-libxml2 -qq
sudo apt-get install gnome-core-devel gnome-devel -qq
sudo apt-get install anjuta glade devhelp -qq
sudo apt-get install gstreamer0.10-plugins-bad gstreamer0.10-plugins-bad-multiverse -qq
sudo apt-get install libgtk-3-dev libgstreamer0.10-dev libclutter-1.0-dev libwebkitgtk-3.0-dev libgda-5.0-dev -qq
sudo apt-get install libgtk-3-doc gstreamer0.10-doc libclutter-1.0-doc libgda-5.0-doc -qq
sudo apt-get install g++ -qq
sudo apt-get install libgtkmm-3.0-dev libgstreamermm-0.10-dev libgdamm5.0-dev -qq
sudo apt-get install libgtkmm-3.0-doc libgstreamermm-0.10-doc libgdamm5.0-doc -qq
sudo apt-get install python python-gobject -qq

sudo apt-get install git build-essential automake libtool itstool gtk-doc-tools gnome-common gnome-doc-utils yasm flex bison -qq
sudo apt-get install libgirepository1.0-dev python3.2-dev python-gi-dev python3-cairo-dev libcairo2-dev python-gi-cairo libgdk-pixbuf2.0-dev libpulse-dev libgtk-3-dev libclutter-1.0-dev libclutter-gtk-1.0-dev libclutter-gst-1.0-0 libclutter-gst-1.0-dbg libclutter-gst-dev gir1.2-clutter-gst-1.0 libxml2-dev python-numpy gir1.2-clutter-1.0 -qq
sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-alsa gstreamer1.0-pulseaudio libgstreamer-plugins-bad1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstreamer1.0-0 -qq
sudo apt-get install python-gi gstreamer1.0-tools gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad gstreamer1.0-libav -qq
sudo apt-get -qq build-dep gstreamer1.0-plugins-base
sudo apt-get -qq build-dep gstreamer1.0-plugins-good
sudo apt-get -qq build-dep gstreamer1.0-plugins-ugly

sudo apt-get -qq install gstreamer1.0-alsa gstreamer1.0-doc gstreamer1.0-libav gstreamer1.0-libav-dbg gstreamer1.0-plugins-bad gstreamer1.0-plugins-bad-dbg gstreamer1.0-plugins-bad-doc gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-base-dbg gstreamer1.0-plugins-base-doc gstreamer1.0-plugins-good gstreamer1.0-plugins-good-dbg gstreamer1.0-plugins-good-doc gstreamer1.0-plugins-ugly gstreamer1.0-plugins-ugly-dbg gstreamer1.0-plugins-ugly-doc gstreamer1.0-pulseaudio gstreamer1.0-tools gstreamer1.0-x libgstreamer1.0-0 libgstreamer1.0-0-dbg libgstreamer1.0-dev
sudo apt-get -qq install libglu1-mesa-dev python3-gi
sudo apt-get install -qq git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev libpq-dev libmysqlclient-dev
sudo apt-get install -qq libglib2.0-*
sudo apt-get install -qq apt-file
sudo apt-get install -qq python-libxml2
sudo apt-get install -qq gnome-core-devel gnome-devel
sudo apt-get install -qq anjuta glade devhelp
sudo apt-get install -qq gstreamer0.10-plugins-bad gstreamer0.10-plugins-bad-multiverse
sudo apt-get install -qq libgtk-3-dev libgstreamer0.10-dev libclutter-1.0-dev libwebkitgtk-3.0-dev libgda-5.0-dev
sudo apt-get install -qq libgtk-3-doc gstreamer0.10-doc libclutter-1.0-doc libgda-5.0-doc
sudo apt-get install -qq g++
sudo apt-get install -qq libgtkmm-3.0-dev libgstreamermm-0.10-dev libgdamm5.0-dev
sudo apt-get install -qq libgtkmm-3.0-doc libgstreamermm-0.10-doc libgdamm5.0-doc
sudo apt-get install -qq python python-gobject

sudo apt-get install -qq git build-essential automake libtool itstool gtk-doc-tools gnome-common gnome-doc-utils yasm flex bison
sudo apt-get install -qq gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-alsa gstreamer1.0-pulseaudio libgstreamer-plugins-bad1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstreamer1.0-0
sudo apt-get build-dep gstreamer1.0-plugins-base
sudo apt-get build-dep gstreamer1.0-plugins-ugly
sudo apt-get install -qq libglu1-mesa-dev
sudo apt-get install -qq automake pkg-config libpcre3-dev zlib1g-dev liblzma-dev
sudo apt-get install -qq build-essential autotools-dev automake autoconf libtool autopoint libxml2-dev zlib1g-dev libglib2.0-dev pkg-config bison flex python git gtk-doc-tools libasound2-dev libgudev-1.0-dev libxt-dev libvorbis-dev libcdparanoia-dev libpango1.0-dev libtheora-dev libvisual-0.4-dev iso-codes libgtk-3-dev libraw1394-dev libiec61883-dev libavc1394-dev libv4l-dev libcairo2-dev libcaca-dev libspeex-dev libpng-dev libshout3-dev libjpeg-dev libaa1-dev libflac-dev libdv4-dev libtag1-dev libwavpack-dev libpulse-dev libsoup2.4-dev libbz2-dev libcdaudio-dev libdc1394-22-dev ladspa-sdk libass-dev libcurl4-gnutls-dev libdca-dev libdirac-dev libdvdnav-dev libexempi-dev libexif-dev libfaad-dev libgme-dev libgsm1-dev libiptcdata0-dev libkate-dev libmimic-dev libmms-dev libmodplug-dev libmpcdec-dev libofa0-dev libopus-dev librsvg2-dev librtmp-dev libschroedinger-dev libslv2-dev libsndfile1-dev libsoundtouch-dev libspandsp-dev libx11-dev libxvidcore-dev libzbar-dev libzvbi-dev liba52-0.7.4-dev libcdio-dev libdvdread-dev libmad0-dev libmp3lame-dev libmpeg2-4-dev libopencore-amrnb-dev libopencore-amrwb-dev libsidplay1-dev libtwolame-dev libx264-dev
sudo apt-get install -qq libgirepository1.0-dev gstreamer1.0-plugins-good gir1.2-clutter-1.0 gir1.2-clutter-gst-1.0 gir1.2-gtkclutter-1.0 gir1.2-gtksource-3.0 gir1.2-vte-2.90 gir1.2-webkit-1.0 gir1.2-webkit-3.0
sudo apt-get install -qq gstreamer1.0 gstreamer1.0-plugins-base
sudo apt-get install -qq libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install -qq libpoppler-glib-dev python-gtk2 python-cairo-dev python-gobject-dev python-gobject -y
sudo apt-get install -qq automake pkg-config libpcre3-dev zlib1g-dev liblzma-dev
sudo apt-get install -qq libtheora-dev libogg-dev libvorbis-dev libasound2-dev libjack-dev
sudo apt-get install -qq bogofilter-bdb bogofilter-common dbus-x11 dh-autoreconf faad gir1.2-gda-5.0 gnome-pkg-tools graphviz highlight highlight-common libacl1-dev libattr1-dev libavl-dev libavl1 libcap-dev libclutter-gst-1.0-dbg libclutter-gst-dev libcupsdriver1 libdigest-hmac-perl libgda-5.0-dev libgda-5.0-doc libgdamm-5.0-13 libgdamm5.0-dev libgdamm5.0-doc libgpgme11-dev libgsl0ldbl libgstreamermm-0.10-2 libgstreamermm-0.10-dev libgstreamermm-0.10-doc libiw-dev libjasper1 libmagic1 libmail-spf-perl libmpfr-dev libnet-dns-perl libnet-ip-perl libnetaddr-ip-perl libosmgpsmap-dev libosmgpsmap2 libpam0g-dev libpth-dev libpython3.2 libsasl2-dev libusb-1.0-0-dev libvala-0.12-0 libvala-0.14-0 libvaladoc0 libvpx-dev libwebp-dev libwebp2 libxml++2.6-2 libxml++2.6-dev libxv1 libyaml-dev ppp-dev python-osmgpsmap python3 python3-cairo python3-cairo-dev python3-dev python3-minimal python3.2 python3.2-dev python3.2-minimal ragel re2c spamassassin spamc texinfo texlive texlive-bibtex-extra texlive-math-extra valac valac-0.14 valadoc x11proto-xext-dev xmlto yelp-tools
sudo apt-get install -qq python-gi python3-gi gstreamer1.0-tools gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad gstreamer1.0-libav
sudo apt-get install -qq python-gi gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad gstreamer1.0-libav
sudo apt-get install -qq libxv1 libxv-dev libxvidcore4 libxvidcore-dev faac libfaac-dev libfaad-dev bison libavl-dev yasm flex zlib1g-dev libffi-dev gettext
sudo apt-get install -qq libgstreamer0.10-dev libgstreamer0.10-0-dbg libgstreamer0.10-0 gstreamer0.10-tools gstreamer-tools gstreamer0.10-doc gstreamer0.10-ffmpeg gstreamer0.10-x
sudo apt-get install -qq libmpg123-dev gstreamer1.0-plugins-ugly
sudo apt-get install -qq freeglut3-dev libasound2-dev libxmu-dev libxxf86vm-dev g++ libgl1-mesa-dev libglu1-mesa-dev libraw1394-dev libudev-dev libdrm-dev libglew-dev libopenal-dev libsndfile-dev libfreeimage-dev libcairo2-dev python-lxml python-argparse libfreetype6-dev libssl-dev libpulse-dev libusb-1.0-0-dev libgtk-3-dev
sudo apt-get install -qq gir1.2-gtk-3.0

pip install numpy

curl -L "http://www.cairographics.org/releases/py2cairo-1.10.0.tar.bz2" > py2cairo-1.10.0.tar.bz2
tar xf py2cairo-1.10.0.tar.bz2
cd py2cairo-1.10.0
./waf configure --prefix=$VIRT_ROOT
./waf build
./waf install
cd ..

curl -L "http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.6.tar.bz2" > pygobject-2.28.6.tar.bz2
tar xf pygobject-2.28.6.tar.bz2
cd pygobject-2.28.6
./configure --prefix=$VIRT_ROOT --disable-introspection
make
make install
cd ..

pip install https://github.com/eugeneai/pyxser/archive/master.zip
curl -L "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.32/glib-2.32.4.tar.xz" > glib-2.32.4.tar.xz
tar xf glib-2.32.4.tar.xz
cd glib-2.32.4
./configure --prefix=$VIRT_ROOT
make
make install
cd ..

sudo apt-get install -qqy libtheora-dev libogg-dev libvorbis-dev libasound2-dev libjack-dev
curl -L "http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2" > pygtk-2.24.0.tar.bz2
tar xf pygtk-2.24.0.tar.bz2
cd pygtk-2.24.0
./configure --prefix=$VIRT_ROOT
make
make install
cd ..

curl -L "http://gstreamer.freedesktop.org/src/gst-python/gst-python-1.2.1.tar.gz" > gst-python-1.2.1.tar.gz
tar xf gst-python-1.2.1.tar.gz
cd gst-python-1.2.1
./configure --prefix=$VIRT_ROOT
sudo make
sudo make install
cd ..

export LD_LIBRARY_PATH=$VIRT_ROOT/lib
export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig
export GST_PLUGIN_PATH=$VIRT_ROOT/lib/gstreamer-$GSTREAMER

curl -L "http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz" > sphinxbase-0.8.tar.gz
tar -zxf sphinxbase-0.8.tar.gz
cd sphinxbase-0.8
./configure --prefix=$VIRT_ROOT
make
make install
cd ..

git clone https://github.com/bossjones/bossjones-pocketsphinx.git
cd bossjones-pocketsphinx
./configure --prefix=$VIRT_ROOT
make
make install
cd ..

sudo ldconfig
pip install -r requirements.txt --use-mirrors
pip install -r requirements_plugins.txt --use-mirrors
pip install -r requirements_dev.txt --use-mirrors
pip install ruamel.venvgtk

env | sort
ls -lta $VIRTUAL_ENV/include/
ls -lta $VIRTUAL_ENV/include/*
ls -lta $VIRTUAL_ENV/lib/
ls -lta $VIRTUAL_ENV/lib/*
ls -lta $VIRTUAL_ENV/lib/python2.7/site-packages/
ls -lta $VIRTUAL_ENV/lib/python2.7/site-packages/*

python setup.py install

_SERVERS=( gst-0.10 gstoption.so pygst.pth pygst.py gtk-2.0 glib gobject pygtk.pth pygtk.py pygtk.pyo cairo pocketsphinx.so sphinxbase.so ) && for i in "${_SERVERS[@]}"; do file $VIRTUAL_ENV/lib/python2.7/site-packages/$i; done

python -c 'from gi.repository import Gtk; print Gtk'
python -c 'import gst'
