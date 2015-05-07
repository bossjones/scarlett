#!/bin/bash

export _VIRTUAL_ENV_NAME="scarlett-gst-1.0"
export VIRT_ROOT="$HOME/.virtualenvs/${_VIRTUAL_ENV_NAME}"
export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig

echo $_VIRTUAL_ENV_NAME
echo $VIRT_ROOT
echo $PKG_CONFIG_PATH

_INSTALL_HOME=$HOME/packages
_PS_SRC="${_INSTALL_HOME}/pocketsphinx-0.8"
_GST_SRC="${_INSTALL_HOME}/gstreamer-1.4.5"
_PYCAIRO_SRC="${_INSTALL_HOME}/py2cairo-1.10.0"
#_PYGOBJECT_SRC="${_INSTALL_HOME}/pygobject-3.10.2"
_PYGTK_SRC="${_INSTALL_HOME}/pygtk-2.24.0"
_PYGI_SRC="${_INSTALL_HOME}/pygobject-3.10.2"
_PYGST_SRC="${_INSTALL_HOME}/gst-python-1.4.0"
_PYGLIB_SRC="${_INSTALL_HOME}/glib-2.32.4"

echo $_INSTALL_HOME
echo $_PS_SRC
echo $_GST_SRC
echo $_PYCAIRO_SRC
echo $_PYGTK_SRC
echo $_PYGI_SRC
echo $_PYGST_SRC
echo $_PYGLIB_SRC

# make all dirs
mkdir -p {$_PS_SRC,$_GST_SRC,$_PYCAIRO_SRC,$_PYGTK_SRC,$_PYGST_SRC,$_PYGI_SRC}

# get pocketsphinx
git clone https://github.com/bossjones/bossjones-pocketsphinx.git $_PS_SRC/bossjones-pocketsphinx
#curl 'http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz' > "$_PS_SRC/sphinxbase-0.8.tar.gz"
cd $_PS_SRC
wget  http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
cd -

### # get gst git repos
### git clone git://anongit.freedesktop.org/git/gstreamer/gstreamer
### git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-base
### git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-good
### git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-bad
### git clone git://anongit.freedesktop.org/git/gstreamer/gst-plugins-ugly
### git clone git://anongit.freedesktop.org/git/gstreamer/gst-libav
### git clone git://anongit.freedesktop.org/git/gstreamer/gst-omx

# get py2cairo
curl 'http://www.cairographics.org/releases/py2cairo-1.10.0.tar.bz2' > "$_PYCAIRO_SRC/py2cairo-1.10.0.tar.bz2"

# get pygobject aka PyGi
curl 'http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.10/pygobject-3.10.2.tar.xz' > "$_PYGI_SRC/pygobject-3.10.2.tar.xz"
curl 'http://ftp.acc.umu.se/pub/GNOME/sources/pygobject/3.0/pygobject-3.0.0.tar.xz' > "$_PYGI_SRC/pygobject-3.0.0.tar.xz"

# get pygtk
curl 'https://pypi.python.org/packages/source/P/PyGTK/pygtk-2.24.0.tar.bz2#md5=a1051d5794fd7696d3c1af6422d17a49' > "$_PYGTK_SRC/pygtk-2.24.0.tar.bz2"
#curl 'http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2' > "$_PYGTK_SRC/pygtk-2.24.0.tar.bz2"

# get python-gst
#curl 'http://gstreamer.freedesktop.org/src/gst-python/gst-python-1.4.0.tar.xz' > "$_PYGST_SRC/gst-python-1.4.0.tar.xz"
#curl 'http://gstreamer.freedesktop.org/src/gst-python/gst-python-1.2.1.tar.xz' > "$_PYGST_SRC/gst-python-1.2.1.tar.xz"
curl 'http://gstreamer.freedesktop.org/src/gst-python/gst-python-1.2.1.tar.gz' > "$_PYGST_SRC/gst-python-1.2.1.tar.gz"

# general updates

sudo add-apt-repository -y ppa:gstreamer-developers/ppa
sudo apt-get update
sudo apt-get install -y bash-completion swig
pip install tox sphinx

# Get the required libraries
sudo apt-get install -y build-essential autotools-dev automake autoconf \
                                    libtool autopoint libxml2-dev zlib1g-dev libglib2.0-dev \
                                    pkg-config bison flex python git gtk-doc-tools libasound2-dev \
                                    libgudev-1.0-dev libxt-dev libvorbis-dev libcdparanoia-dev \
                                    libpango1.0-dev libtheora-dev libvisual-0.4-dev iso-codes \
                                    libgtk-3-dev libraw1394-dev libiec61883-dev libavc1394-dev \
                                    libv4l-dev libcairo2-dev libcaca-dev libspeex-dev libpng-dev \
                                    libshout3-dev libjpeg-dev libaa1-dev libflac-dev libdv4-dev \
                                    libtag1-dev libwavpack-dev libpulse-dev libsoup2.4-dev libbz2-dev \
                                    libcdaudio-dev libdc1394-22-dev ladspa-sdk libass-dev \
                                    libcurl4-gnutls-dev libdca-dev libdirac-dev libdvdnav-dev \
                                    libexempi-dev libexif-dev libfaad-dev libgme-dev libgsm1-dev \
                                    libiptcdata0-dev libkate-dev libmimic-dev libmms-dev \
                                    libmodplug-dev libmpcdec-dev libofa0-dev libopus-dev \
                                    librsvg2-dev librtmp-dev libschroedinger-dev libslv2-dev \
                                    libsndfile1-dev libsoundtouch-dev libspandsp-dev libx11-dev \
                                    libxvidcore-dev libzbar-dev libzvbi-dev liba52-0.7.4-dev \
                                    libcdio-dev libdvdread-dev libmad0-dev libmp3lame-dev \
                                    libmpeg2-4-dev libopencore-amrnb-dev libopencore-amrwb-dev \
                                    libsidplay1-dev libtwolame-dev libx264-dev

## this instals glib ( I think )
sudo apt-get install -y \
    libgirepository1.0-dev \
    gstreamer1.0-plugins-good \
    gir1.2-clutter-1.0 \
    gir1.2-clutter-gst-1.0 \
    gir1.2-gtkclutter-1.0 \
    gir1.2-gtksource-3.0 \
    gir1.2-vte-2.90 \
    gir1.2-webkit-1.0 \
    gir1.2-webkit-3.0

export PYTHONPATH=/home/pi/.virtualenvs/scarlett-gst-1.0/local/lib/python2.7/site-packages

# install py2cairo
sudo apt-get install -y git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev libpq-dev libmysqlclient-dev
sudo apt-get install -y libglib2.0-*
#### DISABLED # cd $_PYCAIRO_SRC
#### DISABLED # tar xf py2cairo-1.10.0.tar.bz2
#### DISABLED # cd py2cairo-1.10.0
#### DISABLED # ./waf configure --prefix=$VIRT_ROOT > /dev/null
#### DISABLED # ./waf build > /dev/null
#### DISABLED # ./waf install > /dev/null

cd $_PYCAIRO_SRC
cd py2cairo*
./waf configure --prefix=$VIRT_ROOT > /dev/null
./waf build > /dev/null
./waf install > /dev/null

# Install the latest version of glib (2.32 is required)
#wget http://ftp.gnome.org/pub/gnome/sources/glib/2.34/glib-2.34.1.tar.xz
wget http://ftp.acc.umu.se/pub/gnome/sources/glib/2.32/glib-2.32.4.tar.xz
#cd glib-2.34.1
cd glib-2.32.4
#./configure --prefix=/usr
./configure --prefix=$VIRT_ROOT > /dev/null
make
make install
sudo apt-get install -y libtheora-dev libogg-dev libvorbis-dev  libasound2-dev libjack-dev



#### DISABLE # # install pygtk
#### DISABLE # tar xf pygtk-2.24.0.tar.bz2
#### DISABLE # cd $_PYGTK_SRC
#### DISABLE # cd pygtk-2.24.0
#### DISABLE # ./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig > /dev/null
#### DISABLE # make > /dev/null
#### DISABLE # make install > /dev/null

cd $_PYGI_SRC
tar xf pygobject-2.32.4.tar.xz
cd pygobject-2.32.4
./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig > /dev/null
make > /dev/null
make install > /dev/null



##### DISABLED # #install pygobject
##### DISABLED # cd $_PYGI_SRC
##### DISABLED # tar xf pygobject-3.10.2.tar.xz
##### DISABLED # cd pygobject-3.10.2
##### DISABLED # # DISABLED # ./configure --prefix=$VIRT_ROOT
##### DISABLED # ./configure --prefix=$VIRT_ROOT --disable-introspection > /dev/null
##### DISABLED # make > /dev/null
##### DISABLED # make install > /dev/null

# MIGHT NOT NEED THIS
cd $_PYGTK_SRC
tar xf pygtk-2.24.0.tar.bz2
cd pygtk-2.24.0
# DISABLED # ./configure --prefix=$VIRT_ROOT > /dev/null
#./configure --prefix=$VIRTUAL_ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig > /dev/null
./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig
make > /dev/null
make install > /dev/null

sudo apt-get -y install git build-essential automake libtool itstool gtk-doc-tools gnome-common gnome-doc-utils yasm flex bison
sudo apt-get -y install python-gst0.10 python-gst0.10-dev gstreamer0.10-plugins-good
sudo apt-get -y install gstreamer0.10-ffmpeg gstreamer-tools gstreamer0.10-alsa gstreamer0.10-nice gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly gstreamer0.10-tools libgstreamer-plugins-bad0.10-0 libgstreamer-plugins-bad0.10-dev libgstreamer-plugins-base0.10-0 libgstreamer-plugins-base0.10-dev libgstreamer0.10-0 libgstreamer0.10-0-dbg libgstreamer0.10-cil-dev libgstreamer0.10-dev libgstrtspserver-0.10-0 libgstrtspserver-0.10-dev libnice-dev
sudo apt-get -y install gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly
sudo apt-get -y install gstreamer0.10-pulseaudio
sudo apt-get -y install gstreamer0.10-alsa
sudo apt-get -y install pavucontrol gstreamer0.10-pulseaudio pulseaudio
sudo apt-get -y install gstreamer0.10-pulseaudio libao4 libasound2-plugins libgconfmm-2.6-1c2 libglademm-2.4-1c2a libpulse-dev libpulse-mainloop-glib0 libpulse-mainloop-glib0-dbg libpulse0 libpulse0-dbg libsox-fmt-pulse paman paprefs pavucontrol pavumeter pulseaudio pulseaudio-dbg pulseaudio-esound-compat pulseaudio-esound-compat-dbg pulseaudio-module-bluetooth pulseaudio-module-gconf pulseaudio-module-jack pulseaudio-module-lirc pulseaudio-module-lirc-dbg pulseaudio-module-x11 pulseaudio-module-zeroconf pulseaudio-module-zeroconf-dbg pulseaudio-utils
sudo apt-get -y install bison
sudo apt-get -y install autoconf automake bison build-essential libasound2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libtool python-gst0.10 python-pyside python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-iplib python-simplejson
sudo apt-get -y install python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-pip python-setuptools python-gtk2 python-yaml python-yaml-dbg
sudo apt-get -y install python2.7-dev
sudo apt-get -y install bison

sudo apt-get update



# install gstreamer-1.0
sudo apt-get -y install gstreamer1.0* libgstreamer1.0*
sudo apt-get -y install python-gst1.0 python-gst1.0-dbg python-gst1.0-dev python-gst1.0-rtsp python-pip python-setuptools
sudo apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

sudo apt-get install -y libusb-1.0

# install gst-python

cd $_PYGST_SRC
tar xvf gst-python-1.2.1.tar.gz
cd gst-python-1.2.1
#./configure --prefix=$VIRT_ROOT
./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRT_ROOT/lib/pkgconfig
make > /dev/null
make install > /dev/null

# import
python -c 'from gi.repository import Gtk; print Gtk'
python -c 'import gst'

# install pocketsphinx
export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-1.0
cd $_PS_SRC

# sphinxbase
tar -zxf sphinxbase-0.8.tar.gz
cd sphinxbase-0.8
# might need just ./configure
#./configure --prefix=$VIRT_ROOT
./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRT_ROOT/lib/pkgconfig
make
make install

# pocketsphinx
cd $_PS_SRC
cd bossjones-pocketsphinx
# might need just ./configure
#./configure --prefix=$VIRT_ROOT
./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig
make
make install
cd ..
# might need sudo ldconfig
ldconfig

cd /home/pi/dev/bossjones-github/scarlett
pip install -r requirements_dev.txt --use-mirrors
pip install -r requirements.txt --use-mirrors
pip install -r requirements.txt





cd $HOME
mkdir packages
cd packages
mkdir gstreamer-1.2
cd gstreamer-1.2
