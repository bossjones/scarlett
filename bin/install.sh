#!/bin/bash

_DATE=$(date '+%Y%m%d.%H%M%S')

git config --global user.name ${_GIT_USER_NAME};
git config --global user.email ${_GIT_EMAIL};
git config --global github.user ${GIT_USER};
git config --global github.token ${_GIT_TOKEN};

# 10/13/2014 - get gstreamer dependencies -- SOURCE: http://wiki.pitivi.org/wiki/GStreamer_from_Git
# apt-cache search --names-only '^(lib)?gstreamer\S*' | sed 's/\(.*\) -.*/\1 /' > dependencies
# sudo apt-get build-dep `cat dependencies`


# 3. check authentication:
ssh -T git@github.com -o StrictHostKeyChecking=no

if [[ ! -d "/usr/local/src/sphinxbase-0.8" ]]; then
   cd /usr/local/src/
   sudo wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
   sudo tar -xvf sphinxbase-0.8.tar.gz
   cd -
fi

if [[ ! -d "/usr/local/src/pocketsphinx-0.8" ]]; then
  cd /usr/local/src/
  sudo wget http://sourceforge.net/projects/cmusphinx/files/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
  sudo tar -xvf pocketsphinx-0.8.tar.gz
  cd -
fi

sudo chown pi:pi /usr/local/src/pocketsphinx-0.8 -R;
sudo chown pi:pi /usr/local/src/sphinxbase-0.8 -R;

#### # uninstall sphinxbase
#### cd /usr/local/src
#### cd sphinxbase-0.8
#### make clean
#### sudo make uninstall
#### cd -
####
#### # uninstall pocketsphinx
#### cd pocketsphinx-0.8
#### make clean
#### sudo make uninstall
#### cd -

sudo apt-get install -y gstreamer0.10-alsa gstreamer-tools gst123;
sudo apt-get install -y gstreamer-tools gstreamer0.10-plugins-bad gstreamer0.10-plugins-good v4l-utils;
sudo apt-get install -y gstreamer0.10-plugins-bad* gstreamer0.10-plugins-base* gstreamer0.10-plugins-good* gstreamer0.10-plugins-ugly*;

sudo apt-get install -y alsa-tools alsa-utils alsa-firmware-loaders libasound2-plugin-equal libasound2-plugins;
sudo apt-get install -y alsa-tools alsa-oss flex zlib1g-dev libc-bin libc-dev-bin python-pexpect libasound2 libasound2-dev cvs;
sudo apt-get install -y mpg321;
sudo apt-get install -y lame;
sudo apt-get install -y sox mplayer ffmpeg;
sudo apt-get install -y alsa-oss alsaplayer mpg321 alsaplayer-alsa alsa-base;
sudo apt-get install -y gstreamer0.10-ffmpeg gstreamer-tools gstreamer0.10-alsa gstreamer0.10-nice gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly gstreamer0.10-tools libgstreamer-plugins-bad0.10-0 libgstreamer-plugins-bad0.10-dev libgstreamer-plugins-base0.10-0 libgstreamer-plugins-base0.10-dev libgstreamer0.10-0 libgstreamer0.10-0-dbg libgstreamer0.10-cil-dev libgstreamer0.10-dev libgstrtspserver-0.10-0 libgstrtspserver-0.10-dev libnice-dev;
sudo apt-get install -y pavucontrol gstreamer0.10-pulseaudio pulseaudio;
sudo apt-get install -y youtube-dl axel curl xterm libcurl4-gnutls-dev mpg123 flac sox;
sudo apt-get install -y gstreamer0.10-pulseaudio libao4 libasound2-plugins libgconfmm-2.6-1c2 libglademm-2.4-1c2a libpulse-dev libpulse-mainloop-glib0 libpulse-mainloop-glib0-dbg libpulse0 libpulse0-dbg libsox-fmt-pulse paman paprefs pavucontrol pavumeter pulseaudio pulseaudio-dbg pulseaudio-esound-compat pulseaudio-esound-compat-dbg pulseaudio-module-bluetooth pulseaudio-module-gconf pulseaudio-module-jack pulseaudio-module-lirc pulseaudio-module-lirc-dbg pulseaudio-module-x11 pulseaudio-module-zeroconf pulseaudio-module-zeroconf-dbg pulseaudio-utils;

# change to use pulse audio
sudo \cp -pf /etc/asound.conf /etc/asound.conf.${_DATE}
echo 'pcm.pulse {
    type pulse
}

ctl.pulse {
    type pulse
}

pcm.!default {
    type pulse
}

ctl.!default {
    type pulse
}' | sudo tee /etc/asound.conf

_DISALLOW_MODULE_LOADING=$(grep "DISALLOW_MODULE_LOADING=1" /etc/default/pulseaudio | wc -l)
if [[ "${_DISALLOW_MODULE_LOADING}" = "0" ]]; then

  sudo \cp -pf /etc/default/pulseaudio /etc/default/pulseaudio.${_DATE}
  sudo sed -i "s,DISALLOW_MODULE_LOADING=1,DISALLOW_MODULE_LOADING=0,g" /etc/default/pulseaudio

fi

# This is the important part that prevents PulseAudio from sending the audio hardware to sleep.
sudo sed -i 's,^#load-module module-suspend-on-idle,load-module module-suspend-on-idle,g' /etc/pulse/default.pa

# change default driver frm alsa to pulse
sudo \cp -fvp /etc/libao.conf /etc/libao.conf.${_DATE}
sudo sed -i "s,^default_driver=alsa,default_driver=pulse,g" /etc/libao.conf
cat /etc/libao.conf
echo -e "\n\n\nsleep 10 seconds to see what it looks like!!! "
sleep 10

############### COMMENT OUT FROM HERE #################

# add pi user to audio groups
sudo adduser pi pulse-access

# pre-req's for pocketsphinx
sudo apt-get install -y python2.7-dev;
sudo apt-get install -y bison;

sudo apt-get install -y autoconf automake bison build-essential libasound2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libtool python-gst0.10 python-pyside python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-iplib python-simplejson;

# if python3 is installed, make sure you remove it first
sudo apt-get remove -y python3.2-minimal python3.2 python3-tk python3-rpi.gpio python3-numpy python3-minimal python3;
sudo apt-get install python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-pip python-setuptools python-gtk2 python-yaml python-yaml-dbg -y

export PYTHONPATH=/usr/local/lib/python2.7/site-packages
export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-0.10


_EXISTS=$(grep "export PYTHONPATH=/usr/local/lib/python2.7/site-packages" /home/pi/.bashrc | wc -l)
if [[ "${_EXISTS}" = "0" ]]; then
  echo "export PYTHONPATH=/usr/local/lib/python2.7/site-packages" >> ~/.bashrc
fi

_EXISTS=$(grep 'export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-0.10' /home/pi/.bashrc | wc -l)
if [[ "${_EXISTS}" = "0" ]]; then
  echo 'export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-0.10' >> ~/.bashrc
fi

_EXISTS=$(grep 'export LD_LIBRARY_PATH=/usr/local/lib' /home/pi/.bashrc | wc -l)
if [[ "${_EXISTS}" = "0" ]]; then
  echo 'export LD_LIBRARY_PATH=/usr/local/lib' >> ~/.bashrc
fi

_EXISTS=$(grep 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig' /home/pi/.bashrc | wc -l)
if [[ "${_EXISTS}" = "0" ]]; then
  echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig' >> ~/.bashrc
fi


##################################################################
# sphinxbase install
##################################################################
cd /usr/local/src
cd sphinxbase-0.8
./configure
make
sudo make install

export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig

# make sure we add this to our .bashrc so that it's always loaded when we login
_EXISTS=$(grep "export LD_LIBRARY_PATH=/usr/local/lib" /home/pi/.bashrc | wc -l)
if [[ "${_EXISTS}" = "0" ]]; then
  echo "export LD_LIBRARY_PATH=/usr/local/lib" >> ~/.bashrc
fi

_EXISTS=$(grep "export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig" /home/pi/.bashrc | wc -l)
if [[ "${_EXISTS}" = "0" ]]; then
  echo "export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig" >> ~/.bashrc
fi

# we're going to add a step in here that modifies the default values for the following params THIS IS VERY HACKISH
# wip
# silprob
# best path
# GIVEN THE FOLLOWING: /usr/local/src/pocketsphinx-0.8/include/cmdln_macro.h
_BEST_PATH_LINE_NUMBER=$(grep -n "\-bestpath" /usr/local/src/pocketsphinx-0.8/include/cmdln_macro.h | head -1 | cut -d: -f1)
_LINE_TO_EDIT=$(($_BEST_PATH_LINE_NUMBER+2))
echo $_LINE_TO_EDIT
sudo sed -i "${_LINE_TO_EDIT}s,yes,no," /usr/local/src/pocketsphinx-0.8/include/cmdln_macro.h

_SILPROB_LINE_NUMBER=$(grep -n "\-silprob" /usr/local/src/pocketsphinx-0.8/include/cmdln_macro.h | head -1 | cut -d: -f1)
_LINE_TO_EDIT=$(($_SILPROB_LINE_NUMBER+2))
echo ${_LINE_TO_EDIT}
sudo sed -i "${_LINE_TO_EDIT}s,0.005,0.1," /usr/local/src/pocketsphinx-0.8/include/cmdln_macro.h

_WIP_LINE_NUMBER=$(grep -n "\-wip" /usr/local/src/pocketsphinx-0.8/include/cmdln_macro.h | head -1 | cut -d: -f1)
_LINE_TO_EDIT=$(($_WIP_LINE_NUMBER+2))
echo ${_LINE_TO_EDIT}
sudo sed -i "${_LINE_TO_EDIT}s,0.65,1e-4," /usr/local/src/pocketsphinx-0.8/include/cmdln_macro.h

echo $LD_LIBRARY_PATH
echo $PKG_CONFIG_PATH
echo $PYTHONPATH
echo $LD_LIBRARY_PATH
echo $PKG_CONFIG_PATH
echo $GST_PLUGIN_PATH

# install pockatsphinx now
cd /usr/local/src/
cd pocketsphinx-0.8
./configure
make
sudo make install

# change ownership of pocketsphinx dir:
sudo chown pi:pi -R /usr/local/share/pocketsphinx

sudo apt-get install -y oss-compat;

# more python stuff...alsa bindings? do we need this?
sudo apt-get install -y python-alsaaudio python-pyalsa;

# install dependancies
#### NOT YET #sudo pip install wordnik==2.1.1;
#### NOT YET #sudo pip install wolframalpha;
#### NOT YET #sudo pip install nltk;

# NOTE:

sudo apt-get install -y festival festival-freebsoft-utils;

# install espeak so you can hear speech

sudo apt-get install -y espeak;


# install python modules
cd ~pi/
mkdir -p dev
cd dev
git clone git@github.com:bossjones/scarlett.git

pacmd set-default-source "alsa_input.usb-OmniVision_Technologies__Inc._USB_Camera-B4.09.24.1-01-CameraB409241.analog-4-channel-input"

# install nodejs

sudo apt-get install -y python-software-properties
sudo apt-add-repository -y ppa:chris-lea/node.js
sudo apt-get update

sudo apt-get install -y nodejs nodejs-dev;
sudo apt-get install -y npm;

# lets setup up our arduino on the pi
# based on the following: http://tech.cyborg5.com/2013/05/30/irlib-tutorial-part-3d-installing-the-arduino-ide-on-a-raspberry-pi/
cd ~pi
sudo apt-get install -y arduino;
mkdir -p ~/downloads
cd ~/downloads
wget http://arduino.googlecode.com/files/arduino-1.0.5-linux32.tgz
tar zxvf arduino-1.0.5-linux32.tgz
cd ~/downloads/arduino-1.0.5
rm -rfv ~/downloads/arduino-1.0.5/hardware/tools

sudo cp -ru ~/downloads/arduino-1.0.5/lib /usr/share/arduino
sudo cp -ru ~/downloads/arduino-1.0.5/libraries /usr/share/arduino
sudo cp -ru ~/downloads/arduino-1.0.5/tools /usr/share/arduino
sudo cp -ru ~/downloads/arduino-1.0.5/hardware /usr/share/arduino
sudo cp -ru ~/downloads/arduino-1.0.5/examples /usr/share/doc/arduino-core
sudo cp -ru ~/downloads/arduino-1.0.5/reference /usr/share/doc/arduino-core

cd ~pi

# on ubuntu do this for arduino
sudo adduser pi dialout
sudo adduser pi tty

# suggested: sudo usermod -a -G dialout pi

# install ino instead
# http://joequery.me/code/arduino-ubuntu-virtualbox-windows-host/

sudo apt-get install -y picocom
sudo pip install -y ino;

# here: http://stackoverflow.com/questions/9064289/installing-pygtk-in-virtualenv
#### DO THIS IN VIRTUALENV # wget http://pypi.python.org/packages/source/P/PyGTK/pygtk-2.24.0.tar.bz2
#### DO THIS IN VIRTUALENV # cd pygtk*
#### DO THIS IN VIRTUALENV # export PKG_CONFIG_PATH=/home/PATH/TO/VIRT/lib/pkgconfig
#### DO THIS IN VIRTUALENV # ./configure --prefix=/home/PATH/TO/VIRT/
#### DO THIS IN VIRTUALENV # make
#### DO THIS IN VIRTUALENV # make install

# test using the python-espeak bindings
# http://dodgyville.tumblr.com/post/25814402767/simple-python-espeak-example
# sudo apt-get install espeak python-espeak

# install gstreamer bash completion!!
# https://raw.githubusercontent.com/drothlis/gstreamer/38df76af49f81857c8f0bed3f426093469f5ae01/tools/gstreamer-completion-0.10
# GST_DEBUG=qtdemux:5,faad:5,ffdec_h264:5 gst-launch-0.10 filesrc location=turn_lights_red.mp4 ! qtdemux name=demuxer demuxer. ! queue ! faad ! audioconvert ! audioresample ! audio/x-raw-int, rate=16000,depth=16 ! wavenc ! filesink location=./turn_lights_red.wav

# try integration test gst-launch-0.10 command. play wav file pipe to pocketsphinx
# gst-launch-0.10 playbin2 uri=turn_lights_red.wav ! pocketsphinx lm=/home/pi/dev/bossjones-github/scarlett/scarlett/static/speech/lm/1602.lm dict=/home/pi/dev/bossjones-github/scarlett/scarlett/static/speech/dict/1602.dic hmm=/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k name=listener ! fakesink dump=1

# not fully working
#gst-launch-0.10 filesrc location=turn_lights_red.wav ! audioconvert ! audioresample ! "audio/x-raw-int, rate=16000, width=16, depth=16, channels=1" ! audioresample ! "audio/x-raw-int, rate=8000" ! pocketsphinx lm=/home/pi/dev/bossjones-github/scarlett/scarlett/static/speech/lm/1602.lm dict=/home/pi/dev/bossjones-github/scarlett/scarlett/static/speech/dict/1602.dic hmm=/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k name=listener ! fakesink dump=1

# pocketsphinx_continuous -lm /home/pi/dev/bossjones-github/scarlett/scarlett/static/speech/lm/1602.lm -dict /home/pi/dev/bossjones-github/scarlett/scarlett/static/speech/dict/1602.dic -hmm /usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k -silprob  0.1 -wip 1e-4 -bestpath 0 -samprate 8000 -infile

# install in virtualenv
export VIRT_ROOT=~/.virtualenvs/scarlett-virtualenv
export PKG_CONFIG_PATH=$VIRT_ROOT/lib/pkgconfig
# one liner
# cd /home/pi/dev/bossjones-github/scarlett && sudo apt-get update && sudo apt-get install -y bash-completion swig && pip install tox sphinx && sudo apt-get install -y git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev libpq-dev libmysqlclient-dev && wget http://www.cairographics.org/releases/py2cairo-1.10.0.tar.bz2 && tar xf py2cairo-1.10.0.tar.bz2 && cd py2cairo-1.10.0 && ./waf configure --prefix=$VIRT_ROOT > /dev/null && ./waf build > /dev/null && ./waf install > /dev/null && cd .. && wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.6.tar.bz2 && tar xf pygobject-2.28.6.tar.bz2 && cd pygobject-2.28.6 && ./configure --prefix=$VIRT_ROOT --disable-introspection > /dev/null && make > /dev/null && make install > /dev/null && cd .. && wget http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2 && tar xf pygtk-2.24.0.tar.bz2 && cd pygtk-2.24.0 && ./configure --prefix=$VIRT_ROOT > /dev/null && make > /dev/null && make install > /dev/null && cd .. && sudo apt-get -y install git build-essential automake libtool itstool gtk-doc-tools gnome-common gnome-doc-utils yasm flex bison && sudo apt-get -y install python-gst0.10 python-gst0.10-dev gstreamer0.10-plugins-good && sudo apt-get -y install gstreamer0.10-ffmpeg gstreamer-tools gstreamer0.10-alsa gstreamer0.10-nice gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly gstreamer0.10-tools libgstreamer-plugins-bad0.10-0 libgstreamer-plugins-bad0.10-dev libgstreamer-plugins-base0.10-0 libgstreamer-plugins-base0.10-dev libgstreamer0.10-0 libgstreamer0.10-0-dbg libgstreamer0.10-cil-dev libgstreamer0.10-dev libgstrtspserver-0.10-0 libgstrtspserver-0.10-dev libnice-dev && sudo apt-get -y install gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly && sudo apt-get -y install gstreamer0.10-pulseaudio && sudo apt-get -y install gstreamer0.10-alsa && sudo apt-get -y install pavucontrol gstreamer0.10-pulseaudio pulseaudio && sudo apt-get -y install gstreamer0.10-pulseaudio libao4 libasound2-plugins libgconfmm-2.6-1c2 libglademm-2.4-1c2a libpulse-dev libpulse-mainloop-glib0 libpulse-mainloop-glib0-dbg libpulse0 libpulse0-dbg libsox-fmt-pulse paman paprefs pavucontrol pavumeter pulseaudio pulseaudio-dbg pulseaudio-esound-compat pulseaudio-esound-compat-dbg pulseaudio-module-bluetooth pulseaudio-module-gconf pulseaudio-module-jack pulseaudio-module-lirc pulseaudio-module-lirc-dbg pulseaudio-module-x11 pulseaudio-module-zeroconf pulseaudio-module-zeroconf-dbg pulseaudio-utils && sudo apt-get -y install bison && sudo apt-get -y install autoconf automake bison build-essential libasound2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libtool python-gst0.10 python-pyside python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-iplib python-simplejson && sudo apt-get -y install python-gst0.10 python-gst0.10-dbg python-gst0.10-dev python-gst0.10-rtsp python-pip python-setuptools python-gtk2 python-yaml python-yaml-dbg && sudo apt-get -y install python2.7-dev && sudo apt-get -y install bison && wget http://gstreamer.freedesktop.org/src/gst-python/gst-python-0.10.22.tar.bz2 && tar xvf gst-python-0.10.22.tar.bz2 && cd gst-python-0.10.22 && ./configure --prefix=$VIRT_ROOT && make > /dev/null && make install > /dev/null && cd .. && python -c 'import pygst' && python -c 'import gst' && wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz && tar -zxf sphinxbase-0.8.tar.gz && cd sphinxbase-0.8 && ./configure && make && sudo make install && cd .. && git clone https://github.com/bossjones/bossjones-pocketsphinx.git && cd bossjones-pocketsphinx && ./configure && make && sudo make install && cd .. && sudo ldconfig && pip install -r requirements_dev.txt --use-mirrors && pip install -r requirements.txt --use-mirrors && pip install -r requirements_plugins.txt --use-mirrors
cd /home/pi/dev/bossjones-github/scarlett
sudo apt-get update
sudo apt-get install -y bash-completion swig
pip install tox sphinx
sudo apt-get install -y git libcairo2-dev libgtk2.0-dev libglib2.0-dev libtool libpango1.0-dev libatk1.0-dev libffi-dev libpq-dev libmysqlclient-dev
wget http://www.cairographics.org/releases/py2cairo-1.10.0.tar.bz2
tar xf py2cairo-1.10.0.tar.bz2
cd py2cairo-1.10.0
./waf configure --prefix=$VIRT_ROOT > /dev/null
./waf build > /dev/null
./waf install > /dev/null
cd ..
wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.6.tar.bz2
tar xf pygobject-2.28.6.tar.bz2
cd pygobject-2.28.6
./configure --prefix=$VIRT_ROOT --disable-introspection > /dev/null
make > /dev/null
make install > /dev/null
cd ..
wget http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2
tar xf pygtk-2.24.0.tar.bz2
cd pygtk-2.24.0
./configure --prefix=$VIRT_ROOT > /dev/null
make > /dev/null
make install > /dev/null
cd ..
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
wget http://gstreamer.freedesktop.org/src/gst-python/gst-python-0.10.22.tar.bz2
tar xvf gst-python-0.10.22.tar.bz2
cd gst-python-0.10.22
./configure --prefix=$VIRT_ROOT
make > /dev/null
make install > /dev/null
cd ..
python -c 'import pygst'
python -c 'import gst'
wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
tar -zxf sphinxbase-0.8.tar.gz
cd sphinxbase-0.8
./configure
make
sudo make install
cd ..
git clone https://github.com/bossjones/bossjones-pocketsphinx.git
cd bossjones-pocketsphinx
./configure
make
sudo make install
cd ..
sudo ldconfig
pip install -r requirements_dev.txt --use-mirrors
pip install -r requirements.txt --use-mirrors
pip install --allow-all-external -r requirements.txt
