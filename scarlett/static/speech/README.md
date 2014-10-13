# I used this site to create my .dic/.lm files to use w/ procketsphinx http://www.speech.cs.cmu.edu/tools/lmtool.html

# After running the conversion tool this is what I got:
## 
## Sphinx knowledge base
## 
## Your request for a Sphinx knowledge base appears to have been processed successfully. 
## Note that the following set of files forms a self-consistent configuration and should be used as a unit. 
## 
## The base name for your set is 6404
## 
## Sentences
## Dictionary
## Language Model
## For your convenience there is also a gzip'd tar file version of the above set. 
## You can find log files here. You should examine these for possible errors.
## 
## IMPORTANT: 
## Please download these files as soon as possible; they will be deleted in approximately a half hour.

## NOTE, before running with pocket sphinx: 
## Ok, now fire up your terminal, set the LD_LIBRARY_PATH if you haven’t added it to your .bashrc already and let’s get going!

## ALSO NOTE, regarding the hmm argument, it should be something like this:

## -hmm model/hmm/en_US/hub4wsj_sc_8k