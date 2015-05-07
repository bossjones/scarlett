#!/bin/bash

### setup scarlett on os x
# NOTE: YOU MUST BE USING HOMEBREWED PYTHON
## brew install mopidy
## brew install python-dbus
## brew reinstall homebrew/versions/gst-plugins-good010 --with-check --with-aalib --with-libcdio --with-libdv
## brew reinstall gst-plugins-ugly010 --with-a52dec --with-aalib --with-cdparanoia --with-flac --with-gtk+ --with-jpeg --with-lame --with-libcaca --with-libdvdread --with-libmms --with-libmpeg2 --with-liboil --with-libshout --with-libvorbis --with-mad --with-opencore-amr --with-pango --with-sdl --with-theora --with-two-lame --with-x264
## brew install bossjones-cmu-sphinxbase bossjones-cmu-pocketsphinx

# source: https://github.com/mopidy/mopidy/issues/888
## brew link --overwrite gst-plugins-bad010
## brew link --overwrite gsettings-desktop-schemas
#
# FOLLOWUP
# http://jonathankulp.org/blog.html
# http://ubuntuforums.org/showthread.php?t=1210553
# https://docs.mopidy.com/en/v0.8.1/installation/gstreamer/
# https://github.com/Homebrew/homebrew/tree/master/Library/Formula
# https://github.com/Homebrew/homebrew/blob/master/Library/Formula/cmu-sphinxbase.rb
# https://github.com/Homebrew/homebrew/blob/master/Library/Formula/cmu-pocketsphinx.rb
# https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/FAQ.md
# http://userprimary.net/posts/2009/09/28/writing-packages-for-homebrew-on-os-x/
# https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/Formula-Cookbook.md#formula-cookbook

_VENV_NAME=scarlett-dbus
_PATH_TO_SPHINXBASE=~/dev/bossjones/bossjones-sphinxbase/
_PATH_TO_POCKETSPHINX=~/dev/bossjones/bossjones-pocketsphinx/

# install dbus in virtualenv site-packages
sudo cp -rv /usr/local/lib/python2.7/site-packages/dbus /Users/malcolm/.virtualenvs/${_VENV_NAME}/lib/python2.7/site-packages/
sudo cp -rv /usr/local/lib/python2.7/site-packages/_dbus_*.so /Users/malcolm/.virtualenvs/${_VENV_NAME}/lib/python2.7/site-packages/

# gst-0.10 glib gobject cairo site-packages
sudo cp -rv /usr/local/lib/python2.7/site-packages/{gst-0.10,gstoption.so,pygst.pth,pygst.py,gtk-2.0,glib,gobject,pygtk.pth,pygtk.py,pygtk.pyo,cairo,pocketsphinx.so,sphinxbase.so} /Users/malcolm/.virtualenvs/${_VENV_NAME}/lib/python2.7/site-packages/
sudo cp -rv /usr/local/Cellar/bossjones-cmu-pocketsphinx/0.82/lib/gstreamer-0.10/libgstpocketsphinx* ~/.virtualenvs/scarlett-dbus/lib/gstreamer-0.10/

# install pocketsphinx
#export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-0.10
export VIRT_ROOT=~/.virtualenvs/${_VENV_NAME}
cd ${_PATH_TO_SPHINXBASE}
./configure --prefix=$VIRT_ROOT
make
make install

cd ${_PATH_TO_POCKETSPHINX}
./configure --prefix=$VIRT_ROOT
make
make install
