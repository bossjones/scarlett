cd ~/package
git clone git://git.gnome.org/jhbuild
cd jhbuild
sudo apt-get install yelp-tools -y
./autogen.sh
make
make install

#### Consider adjusting the PKG_CONFIG_PATH environment variable if you
#### installed software in a non-standard prefix.
####
#### Alternatively, you may set the environment variables PYCAIRO_CFLAGS
#### and PYCAIRO_LIBS to avoid the need to call pkg-config.
#### See the pkg-config man page for more details.

#sudo apt-get install gnutls WebKit1 xcb p11-kit
sudo apt-get install python3 python3-dev -y
sudo apt-get install apt-file -y
sudo apt-get install python-libxml2 -y
sudo apt-file update

sudo apt-get install gnome-core-devel gnome-devel -y
sudo apt-get install anjuta glade devhelp -y
sudo apt-get install gstreamer0.10-plugins-bad gstreamer0.10-plugins-bad-multiverse -y
sudo apt-get install libgtk-3-dev libgstreamer0.10-dev libclutter-1.0-dev libwebkitgtk-3.0-dev libgda-5.0-dev -y
sudo apt-get install libgtk-3-doc gstreamer0.10-doc libclutter-1.0-doc libgda-5.0-doc -y
sudo apt-get install g++ -y
sudo apt-get install libgtkmm-3.0-dev libgstreamermm-0.10-dev libgdamm5.0-dev -y
sudo apt-get install libgtkmm-3.0-doc libgstreamermm-0.10-doc libgdamm5.0-doc -y
sudo apt-get install python python-gobject -y
sudo apt-get install git build-essential automake libtool itstool gtk-doc-tools gnome-common gnome-doc-utils yasm flex bison -y

sudo apt-get install libgirepository1.0-dev python3.2-dev python-gi-dev \
python3-cairo-dev libcairo2-dev python-gi-cairo \
libgdk-pixbuf2.0-dev libpulse-dev libgtk-3-dev \
libclutter-1.0-dev libclutter-gtk-1.0-dev \
libclutter-gst-1.0-0 libclutter-gst-1.0-dbg libclutter-gst-dev gir1.2-clutter-gst-1.0 \
libxml2-dev python-numpy gir1.2-clutter-1.0 -y

sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-alsa gstreamer1.0-pulseaudio \
libgstreamer-plugins-bad1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstreamer1.0-0 -y

# GStreamer plugins' full set of dependencies to build all the codecs:
sudo apt-get build-dep gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
sudo apt-get install libglu1-mesa-dev

echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc


curl "https://download.gnome.org/teams/releng/3.15.3/sample-tarball.jhbuildrc" > ~/.jhbuildrc
curl -L "https://download.gnome.org/teams/releng/3.15.3/gnome-apps-3.15.3.modules" > ~/packages/jhbuild/modulesets/gnome-apps-3.15.3.modules
curl -L "https://download.gnome.org/teams/releng/3.15.3/gnome-suites-core-3.15.3.modules" > ~/packages/jhbuild/modulesets/gnome-suites-core-3.15.3.modules
curl -L "https://download.gnome.org/teams/releng/3.15.3/gnome-suites-core-deps-3.15.3.modules" > ~/packages/jhbuild/modulesets/gnome-suites-core-deps-3.15.3.modules
curl -L "https://download.gnome.org/teams/releng/3.15.3/gnome-sysdeps-3.15.3.modules" > ~/packages/jhbuild/modulesets/gnome-sysdeps-3.15.3.modules

# NOTE: IN SCARLETT VIRTUALENV
pip install http://xmlsoft.org/sources/python/libxml2-python-2.6.21.tar.gz


PYTHON=/usr/bin/python jhbuild build pygobject
PYTHON=/usr/bin/python jhbuild build gtk+

export _VIRTUAL_ENV_NAME="scarlett-update"
export VIRT_ROOT="$HOME/.virtualenvs/${_VIRTUAL_ENV_NAME}"
#export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig

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

###### ==========================================================================
###### ==========================================================================
###### ==========================================================================
###### ==========================================================================

cd $_PYCAIRO_SRC
cd py2cairo*
CFLAGS=-I/usr/include/cairo/ ./waf configure --prefix=$VIRT_ROOT > /dev/null
#CFLAGS=-I/usr/include/cairo/ ./configure --prefix=$VIRT_ROOT
./waf build > /dev/null
./waf install > /dev/null

cd $_PYGI_SRC
#tar xf pygobject-2.32.4.tar.xz
#cd pygobject-2.32.4
cd pygobject-3.10.2
#./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig > /dev/null
#./configure --prefix=$VIRT_ROOT --disable-introspection
PYCAIRO_LIBS=$VIRT_ROOT/include/pycairo/ PYCAIRO_CFLAGS=-I$VIRT_ROOT/pycairo/ CFLAGS=-I/usr/include/cairo/ ./configure --prefix=$VIRT_ROOT
make > /dev/null
make install > /dev/null

cd $_PYGST_SRC
#tar xvf gst-python-1.4.0.tar.gz
#cd gst-python-1.4.0
cd gst-python-1.1.90
#./configure --prefix=$VIRT_ROOT
#./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig
./autogen.sh
PYGOBJECT_LIBS=$VIRT_ROOT/include/pygobject-3.0/ PYGOBJECT_CFLAGS=-I$VIRT_ROOT/include/pygobject-3.0/ ./configure --prefix=$VIRT_ROOT
make > /dev/null
make install > /dev/null


# cd ~/package/glib-2.32.4/glib-2.32.4
# cd glib-2.32.4
# #./configure --prefix=/usr
# ./configure --prefix=$VIRT_ROOT > /dev/null
# make
# make install


cd $_PYGTK_SRC
tar xf pygtk-2.24.0.tar.bz2
cd pygtk-2.24.0
# DISABLED # ./configure --prefix=$VIRT_ROOT > /dev/null
#./configure --prefix=$VIRTUAL_ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig > /dev/null
./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig
make > /dev/null
make install > /dev/null


cd $_PYGST_SRC
tar xvf gst-python-1.2.1.tar.gz
cd gst-python-1.2.1
./configure --prefix=$VIRT_ROOT
#./configure --prefix=$VIRT_ROOT PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$VIRTUAL_ENV/lib/pkgconfig
make > /dev/null
make install > /dev/null
