require "formula"

class BossjonesGstPluginsEspeak < Formula
  homepage "http://download.sugarlabs.org/"
  url "https://github.com/bossjones/bossjones-gst-plugins-espeak/archive/0.3.5.tar.gz"
  sha1 "1e939fd3117343c0f654b02565597f575596c972"
  version "0.3.5"

  # We only have special support for finding depends_on :python, but not yet for
  # :ruby, :perl etc., so we use the standard environment that leaves the
  # PATH as the user has set it right now.
  env :std

  head do
    url "https://github.com/bossjones/bossjones-gst-plugins-espeak.git"

    depends_on "autoconf" => :build
    depends_on "automake" => :build
    depends_on "libtool" => :build
    depends_on "swig" => :build
    depends_on "openssl"
  end

  depends_on "pkg-config" => :build
  # If these are found, they will be linked against and there is no configure
  # switch to turn them off.
  depends_on "libsndfile"
  depends_on "libsamplerate" => "with-libsndfile"

  def install
    if build.head?
      ENV["NOCONFIGURE"] = "yes"
      system "./autogen.sh"
    end
    system "./configure", "--disable-debug",
                          "--disable-dependency-tracking",
                          "--prefix=#{prefix}"
    system "make"
    system "make install"
  end
end
