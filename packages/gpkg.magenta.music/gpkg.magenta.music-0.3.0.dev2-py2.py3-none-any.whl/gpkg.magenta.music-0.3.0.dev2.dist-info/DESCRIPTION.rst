
Models
######

magenta-melody
##############

*Applies language modeling to melody generation using an LSTM*

Operations
==========

generate
^^^^^^^^

*Compose melodies using one of three available pretrained models*

Flags
-----

**config**
  *Model configuration (basic, lookback, or attention) (default is
  'basic_rnn')*

**outputs**
  *Number of melodies to generate (default is 10)*

**primary-midi**
  *MIDI file used to prime the generator*

**primer-melody**
  *Melody to prime the generator*

**steps**
  *Melody length (16 steps = 1 bar) (default is 128)*



