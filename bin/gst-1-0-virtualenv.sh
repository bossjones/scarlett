#!/bin/bash

PYTHON_VERSION=2
PYTHON=python$PYTHON_VERSION
VIRT_PREF="(dme)"

export PATH="/usr/local/sbin:$PATH"

###### # virtualenv
###### export WORKON_HOME=$HOME/.virtualenvs
###### export PROJECT_HOME=$HOME/dev
###### export VIRTUALENVWRAPPER_PYTHON=$PYTHON
###### export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
###### export VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh
###### source /usr/local/bin/virtualenvwrapper.sh
###### export PYTHONSTARTUP=~/.pythonrc

PYGOBJECT_V="3.8.3"
CAIRO_V="1.10.0"

VIRT_ROOT="$HOME/.virtualenvs/scarlett-update2"
#export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig

export LC_ALL=C

if [ ! -e $VIRT_ROOT/bin/activate ]; then
    VE=virtualenv-2.7
    VE=$(which $VE)
    if [ "x$VE" = "x" ] ; then
        echo "There are no virtualenv executable."
        echo "Please install it in your distribution or"
        echo "read http://www.virtualenv.org/"
        exit 0
    fi
    #if [ ! -x "$VE" ]; then
    #    echo "Virtualenv script is found but it is not"
    #    echo "executable. please check $VE."
    #fi
    echo "Installing virtual environment into $VIRT_ROOT"
    $VE $VIRT_ROOT --prompt=$VIRT_PREF
fi

# workon scarlett-update


echo $VIRT_ROOT
echo $PKG_CONFIG_PATH

SCARLETT_APP_HOME="/home/pi/dev/bossjones-github/scarlett"

_PYCAIRO_VERSION=$CAIRO_V
#export _PYGOBJECT_VERSION=3.0.0
#export _GST_PYTHON_VERSION=1.2.1

echo $_PYCAIRO_VERSION
#echo $_PYGOBJECT_VERSION
#echo $_GST_PYTHON_VERSION

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

sudo apt-get install -y git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev libpq-dev libmysqlclient-dev
sudo apt-get install -y libglib2.0-*


cd /home/pi/dev/bossjones-github/scarlett

pip install numpy

$PYTHON -c "import cairo"
rc=$?

if [ $rc -ne 0 ]; then
  echo "Installing PY2CAIRO."
  cd /home/pi/dev/bossjones-github/scarlett
  curl -L "http://www.cairographics.org/releases/py2cairo-${_PYCAIRO_VERSION}.tar.bz2" > "${SCARLETT_APP_HOME}/py2cairo-${_PYCAIRO_VERSION}.tar.bz2"
  tar xvf py2cairo-$_PYCAIRO_VERSION.tar.bz2
  cd py2cairo-$_PYCAIRO_VERSION
  #./waf configure --prefix=$VIRT_ROOT > /dev/null
  #CFLAGS=-I/usr/include/cairo/ ./waf configure --prefix=$VIRT_ROOT > /dev/null
  ./waf configure --prefix=$VIRT_ROOT
  ./waf build
  ./waf install
  cd ..
  rm -rf $SCARLETT_APP_HOME/py2cairo-$_PYCAIRO_VERSION
fi

$PYTHON -c "import gi"
rc=$?
if [ $rc -ne 0 ]; then

    echo "Installing PyGTK3."
    cd /home/pi/dev/bossjones-github/scarlett
    #wget -c http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.8/pygobject-$PYGOBJECT_V.tar.xz
    curl -L "http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.8/pygobject-$PYGOBJECT_V.tar.xz" > "${SCARLETT_APP_HOME}/pygobject-${PYGOBJECT_V}.tar.xz"
    tar xJf pygobject-$PYGOBJECT_V.tar.xz
    rc=$?
    if [ $rc -ne 0 ]; then
      echo "Code was: ${rc}"
      exit 1
    fi
    cd pygobject-$PYGOBJECT_V
    PYTHON=$VIRT_ROOT/bin/$PYTHON ./configure --prefix=$VIRT_ROOT
    make install
    cd ..
    #rm -rf $SCARLETT_APP_HOME/pygobject-$PYGOBJECT_V
fi

$PYTHON -c "import pyxser"
rc=$?
if [ $rc -ne 0 ]; then

    echo "Installing pyxser."

    pip install https://github.com/eugeneai/pyxser/archive/master.zip
fi

cd ..

#### DISABLED # curl -L "http://ftp.acc.umu.se/pub/GNOME/sources/pygobject/3.0/pygobject-${_PYGOBJECT_VERSION}.tar.xz" > "${SCARLETT_APP_HOME}/pygobject-${_PYGOBJECT_VERSION}.tar.xz"
#### DISABLED # tar xvf pygobject-${_PYGOBJECT_VERSION}.tar.xz
#### DISABLED # cd pygobject-${_PYGOBJECT_VERSION}
#### DISABLED # PYCAIRO_LIBS=$VIRT_ROOT/include/pycairo/ PYCAIRO_CFLAGS=-I$VIRT_ROOT/pycairo/ CFLAGS=-I/usr/include/cairo/ ./configure --prefix=$VIRT_ROOT
#### DISABLED # make > /dev/null
#### DISABLED # make install > /dev/null
#### DISABLED # cd ..

###### SUPER TEMPORARY #### sudo apt-get install -y git build-essential automake libtool itstool gtk-doc-tools gnome-common gnome-doc-utils yasm flex bison
###### SUPER TEMPORARY #### sudo apt-get install -y python-gst0.10 python-gst0.10-dev gstreamer0.10-plugins-good
###### SUPER TEMPORARY #### sudo apt-get install -y gstreamer0.10-ffmpeg gstreamer-tools gstreamer0.10-alsa gstreamer0.10-nice gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly gstreamer0.10-tools libgstreamer-plugins-bad0.10-0 libgstreamer-plugins-bad0.10-dev libgstreamer-plugins-base0.10-0 libgstreamer-plugins-base0.10-dev libgstreamer0.10-0 libgstreamer0.10-0-dbg libgstreamer0.10-cil-dev libgstreamer0.10-dev libgstrtspserver-0.10-0 libgstrtspserver-0.10-dev libnice-dev
###### SUPER TEMPORARY #### sudo apt-get install -y gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly
###### SUPER TEMPORARY #### sudo apt-get install -y gstreamer0.10-pulseaudio
###### SUPER TEMPORARY #### sudo apt-get install -y gstreamer0.10-alsa
###### SUPER TEMPORARY #### sudo apt-get install -y pavucontrol gstreamer0.10-pulseaudio pulseaudio
###### SUPER TEMPORARY #### sudo apt-get install -y gstreamer0.10-pulseaudio libao4 libasound2-plugins libgconfmm-2.6-1c2 libglademm-2.4-1c2a libpulse-dev libpulse-mainloop-glib0 libpulse-mainloop-glib0-dbg libpulse0 libpulse0-dbg libsox-fmt-pulse paman paprefs pavucontrol pavumeter pulseaudio pulseaudio-dbg pulseaudio-esound-compat pulseaudio-esound-compat-dbg pulseaudio-module-bluetooth pulseaudio-module-gconf pulseaudio-module-jack pulseaudio-module-lirc pulseaudio-module-lirc-dbg pulseaudio-module-x11 pulseaudio-module-zeroconf pulseaudio-module-zeroconf-dbg pulseaudio-utils
###### SUPER TEMPORARY #### sudo apt-get install -y bison
###### SUPER TEMPORARY #### sudo apt-get install -y autoconf automake bison build-essential libasound2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libtool python-gst0.10 python-pyside python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-iplib python-simplejson
###### SUPER TEMPORARY #### sudo apt-get install -y python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-pip python-setuptools python-gtk2 python-yaml python-yaml-dbg
###### SUPER TEMPORARY #### sudo apt-get install -y python2.7-dev
###### SUPER TEMPORARY #### sudo apt-get install -y bison
###### SUPER TEMPORARY #### export LD_LIBRARY_PATH=$VIRT_ROOT/lib
###### SUPER TEMPORARY #### export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig
###### SUPER TEMPORARY #### export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-1.0
###### SUPER TEMPORARY ####
###### SUPER TEMPORARY #### curl "http://gstreamer.freedesktop.org/src/gst-python/gst-python-${_GST_PYTHON_VERSION}.tar.gz" > "${SCARLETT_APP_HOME}/gst-python-${_GST_PYTHON_VERSION}.tar.gz"
###### SUPER TEMPORARY #### tar xvf gst-python-${_GST_PYTHON_VERSION}.tar.gz
###### SUPER TEMPORARY #### cd gst-python-${_GST_PYTHON_VERSION}
###### SUPER TEMPORARY #### ./configure --prefix=$VIRT_ROOT
###### SUPER TEMPORARY #### make > /dev/null
###### SUPER TEMPORARY #### make install > /dev/null
###### SUPER TEMPORARY #### cd ..
###### SUPER TEMPORARY ####
###### SUPER TEMPORARY #### # import
###### SUPER TEMPORARY #### python -c 'from gi.repository import Gtk; print Gtk'
###### SUPER TEMPORARY ####
###### SUPER TEMPORARY #### #wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
###### SUPER TEMPORARY #### #tar -zxf sphinxbase-0.8.tar.gz
###### SUPER TEMPORARY #### cd sphinxbase-0.8
###### SUPER TEMPORARY #### ./configure
###### SUPER TEMPORARY #### make
###### SUPER TEMPORARY #### sudo make install
###### SUPER TEMPORARY #### cd ..
###### SUPER TEMPORARY #### #git clone https://github.com/bossjones/bossjones-pocketsphinx.git
###### SUPER TEMPORARY #### cd bossjones-pocketsphinx
###### SUPER TEMPORARY #### ./configure
###### SUPER TEMPORARY #### make
###### SUPER TEMPORARY #### sudo make install
###### SUPER TEMPORARY #### cd ..
###### SUPER TEMPORARY #### sudo ldconfig
###### SUPER TEMPORARY #### pip install -r requirements_dev.txt
###### SUPER TEMPORARY #### pip install -r requirements.txt
