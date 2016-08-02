# rpi-walls
Work in progress for an Automata installation, with John Eagle, Cassia Streb, and Janie Geiser.

First install Raspian onto your Raspberry Pi.

To enable wireless on your Raspberry Pi:
----------------------------------------

Either plug an ethernet cable into your Pi, or use the following to enable wireless internet.

    sudo nano /etc/network/interfaces

Then edit your interfaces file to this.

    auto lo

    iface lo inet loopback
    iface eth0 inet dhcp

    allow-hotplug wlan0
    auto wlan0

    iface wlan0 inet dhcp
        wpa-ssid "your network"
        wpa-psk "your passkey"

**Note:** this will change! Eventually it'll be safer to use static IPs, then we don't have to worry about the IPs changing throughout the installlation.

To install ChucK on a Raspberry Pi:
-----------------------------------

After installing Raspbian onto your Pi and enabling with wireless or an ethernet internet connecton, install ChucK with the following command.

    git clone https://github.com/ccrma/chuck

cd into chuck/src

Now we'll have to install the depnedencies.

    sudo apt-get install bison, flex
    sudo apt-get install alsa-base, libaosound2-dev, libasndfile1-dev

There may be others, will confirm.

Now to build the make file.

    sudo make linux-alsa

This will build the makefile for ChucK, now we install it.

    sudo make install linux-alsa

This moves the built makefile into the proper directory. This should be all we need to install ChucK.


Then run this script, or set to run in rc.local:
------------------------------------------------

Will be done shortly.
