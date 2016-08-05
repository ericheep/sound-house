# rpi-sound-house
Work in progress for an installation at Automata, with John Eagle, Cassia Streb, and Janie Geiser.

There are two methods we're attempting so far, the first sends audio data through OSC using the real-time audio programming language, [ChucK](http://chuck.cs.princeton.edu/).

The second sends audio using the [JACK](http://www.jackosx.com/) audio server over a network to the individual Raspberry Pis using [JackTrip](https://ccrma.stanford.edu/software/jacktrip/) (CCRMA developed system for sending streaming audio over the internet). While JackTrip is meant for wired applications, it still (sorta) works for this one.

Install the latest Raspbian (Jessie)
------------------------------------

While this isn't necessarily required for the ChucK implementation, it is definitely required for the JackTrip implementation. Go to the Raspberry Pi and get the latest [NOOBS image](https://www.raspberrypi.org/downloads/noobs/).

Format your microSD card using [SDFormatter](https://www.sdcard.org/downloads/formatter_4/).

Then simply load the contents of the NOOBS `.zip` onto your card.

![drag and drop](copytocard.png)

To enable wireless on a Raspberry Pi
------------------------------------

We'll have to access the interfaces file, and edit it using the built-in editor (Nano). Use the following command to open the interfaces file for editing.

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

**Note:** This might change! Eventually it'll be safer to use static IPs, then we don't have to worry about the IPs changing throughout the installlation. For now it's a quick way to get up and running.

ChucK Implementation
--------------------
--------------------

This is more of a hack than a real solution, the audio that is sent to the Raspberry Pis sounds a bit glitchy as of right now.

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

JACK/JackTrip Implementation
-------------------
-------------------

Install JACK for OSX.

    https://dl.dropboxusercontent.com/u/28869550/JackOSX.0.92_b3.zip

Then install JackTrip. Go here and download the `.zip` file.

    https://github.com/jcacerec/jacktrip/releases

After unzipping the `.zip` file, go to terminal, change to the directory where `jacktrip` is, go to `/bin`, and run the following commands.

    sudo cp jacktrip /usr/bin/
    sudo chmod 755 /usr/bin/jacktrip

If you're on El Capitan, Apple's System Integrity Protection will prevent you from moving anything around in root. To get around this you'll have to reboot, hold `cmd-r`, open up Terminal through utilities, and type in the following.

    csrutil disable
    reboot

More to come, I hope this works.

