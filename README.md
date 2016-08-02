# rpi-sound-house
Work in progress for an installation at Automata, with John Eagle, Cassia Streb, and Janie Geiser.

First install Raspian onto your Raspberry Pi. There are two methods we're attempting so far, the first sends audio data through OSC using the real-time audio programming language, ChucK, the second is to send audio using Jack to the Raspberry Pis.

ChucK Method
------------
------------

To enable wireless on a Raspberry Pi
------------------------------------

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

To install ChucK on a Raspberry Pi
----------------------------------

First we'll have to install some depnedencies.

    sudo apt-get install bison flex
    sudo apt-get install alsa-base libasound2-dev libasndfile1-dev

Clone the ChucK repository to a suitable directory.

    git clone https://github.com/ccrma/chuck

Now we can change to the `chuck/src` directory and build the makefile.

    cd chuck/src
    sudo make linux-alsa

After it is built, install it.

    sudo make install linux-alsa

Then run this script, or set to run in rc.local
-----------------------------------------------

    chuck receiver.ck

And then on the master computer, run the program that sends the audio.

    chuck sender.ck

That's about it! It's not the best quality at the moment, will need to test with a dedicated router and tweak a few other things.

JACK Method
-----------
-----------

Researching.
