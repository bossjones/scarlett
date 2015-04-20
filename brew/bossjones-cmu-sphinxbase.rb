require "formula"

class BossjonesCmuSphinxbase < Formula
  homepage "http://cmusphinx.sourceforge.net/"
  url "https://github.com/bossjones/bossjones-sphinxbase/archive/0.82.tar.gz"
  sha1 "8d914857ed420372b10cd29f84541938519b1a7f"
  version "0.82"
  #depends_on :python if MacOS.version <= :snow_leopard

  # We only have special support for finding depends_on :python, but not yet for
  # :ruby, :perl etc., so we use the standard environment that leaves the
  # PATH as the user has set it right now.
  env :std

  head do
    url "https://github.com/bossjones/bossjones-sphinxbase.git"

    depends_on "autoconf" => :build
    depends_on "automake" => :build
    depends_on "libtool" => :build
    depends_on "swig" => :build
  end

  depends_on "pkg-config" => :build
  # If these are found, they will be linked against and there is no configure
  # switch to turn them off.
  depends_on "libsndfile"
  depends_on "libsamplerate" => "with-libsndfile"

  def install
    #ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python2.7/site-packages"
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
