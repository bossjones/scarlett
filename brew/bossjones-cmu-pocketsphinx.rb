require 'formula'

class BossjonesCmuPocketsphinx < Formula
  homepage 'http://cmusphinx.sourceforge.net/'
  url 'https://github.com/bossjones/bossjones-pocketsphinx/archive/0.82.tar.gz'
  sha1 '74455b3ec7570f1006a9acf0a1fc538502e045d2'
  version "0.82"

  # We only have special support for finding depends_on :python, but not yet for
  # :ruby, :perl etc., so we use the standard environment that leaves the
  # PATH as the user has set it right now.
  env :std

  head do
    url "https://github.com/bossjones/bossjones-pocketsphinx.git"

    depends_on "autoconf" => :build
    depends_on "automake" => :build
    depends_on "libtool" => :build
    depends_on "swig" => :build
  end

  depends_on 'pkg-config' => :build
  #depends_on 'bossjones-cmu-sphinxbase'

  def install
    if build.head?
      ENV["NOCONFIGURE"] = "yes"
      system "./autogen.sh"
    end
    system "./configure", "--disable-dependency-tracking",
                          "--prefix=#{prefix}"
    system "make"
    system "make install"
  end
end
