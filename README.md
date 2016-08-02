# rpi-walls
Work in progress for an Automata installation, with John Eagle, Cassia Streb, and Janie Geiser.

To install ChucK on a Raspberry Pi:

After installing Raspbian onto your Pi, install ChucK with the following command.

    git clone https://github.com/ccrma/chuck

cd into chuck/src

Now we'll have to install the depnedencies.

    sudo apt-get install alsa-base
    sudo apt-get install libaosund2-dev
    sudo apt-get install libasndfile1-dev

There may be others, will confirm.

Now to build the make file.

    sudo make linux-alsa

This will build the makefile for ChucK, now we install it.

    sudo make install linux-alsa

This moves the built makefile into the proper directory. This should be all we need to install ChucK.

