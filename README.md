# rpi-sound-house
Work in progress for an installation at Automata, with John Eagle, Cassia Streb, and Janie Geiser.

First install Raspian onto your Raspberry Pi.

To enable wireless on your Raspberry Pi:
----------------------------------------

We'll have to access the interfaces file, and edit it using the built in editor. Use the following command to open the interfaces file for editing.

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

To save, press `ctrl-x`, when it asks to save, press `y`. Then press `enter` to finish.

**Note:** This will change! Eventually it'll be safer to use static IPs, then we don't have to worry about the IPs changing throughout the installlation. For now it's a quick way to get up and running.

To install ChucK on a Raspberry Pi:
-----------------------------------

First we'll have to install some depnedencies.

    sudo apt-get install bison flex
    sudo apt-get install alsa-base libasound2-dev libasndfile1-dev

Clone to the ChucK repository to a suitable directory.

    git clone https://github.com/ccrma/chuck

And switch to the Raspberry Pi branch of the repo, make sure you're inside the cloned repo when you do this.

    cd chuck
    git checkout rpi

Now we can build the makefile.

    cd src
    sudo make linux-alsa

This will build the makefile for ChucK, then we install it.

    sudo make install linux-alsa

Then run this script, or set to run in rc.local:
------------------------------------------------

Will be done shortly.
