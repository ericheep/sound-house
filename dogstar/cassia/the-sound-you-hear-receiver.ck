// the sound you hear is the you will be replacing
// receiver script

// written by Cassia Streb
// ChucK realization by Eric Heep

// Dog Star 2018
// ~-~-

OscIn in;
OscMsg msg;

// the port for the incoming messages
10001 => in.port;
in.listenAll();

// ~-~-
// audio chain

0.08 => float sineToneGain;
0.1 => float pinkNoiseGain;
0.1 => float greyNoiseGain;
0.7 => float textureGain;
0.3 => float whiteNoiseFadeOutGain;

SinOsc sineTone => Gain master => dac;
SndBuf greyNoise => master => dac;
CNoise pinkNoise => master => dac;
Noise whiteNoiseFadeOut => ADSR env => master => dac;

0.0 => float targetMasterGain;
master.gain(targetMasterGain);

greyNoise.read(me.dir() + "grey-noise.wav");
greyNoise.gain(greyNoiseGain);

SndBuf textures[4];
["fireplace.wav",
 "texture-1.wav",
 "texture-2.wav",
 "sheep.wav"]
 @=> string wavs[];

for (0 => int i; i < 4; i++) {
    textures[i].read(me.dir() + wavs[i]);
    textures[i].gain(textureGain);
    textures[i] => master => dac;
}

fun void clearAllSound() {
    sineTone.gain(0.0);
    pinkNoise.gain(0.0);
    greyNoise.gain(0.0);
    whiteNoiseFadeOut.gain(0.0);
    for (0 => int i; i < 4; i++) {
        textures[i].gain(0.0);
        textures[i].pos(textures[i].samples());
        textures[i].loop(0);
    }
}


fun void easeMasterGain() {
    while(true) {
        10::ms => now;
        if (master.gain() > targetMasterGain) {
            master.gain(master.gain() - 0.005);
        } else if (master.gain() < targetMasterGain) {
            master.gain(master.gain() + 0.005);
        }
    }
}

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            <<< msg.address, "" >>>;
            if (msg.address == "/silence") {
                clearAllSound();
            }
            if (msg.address == "/sineTone") {
                clearAllSound();
                msg.getFloat(0) => float f;
                sineTone.freq(f);
                sineTone.gain(sineToneGain);
            }
            if (msg.address == "/greyNoise") {
                clearAllSound();
                greyNoise.pos(Math.random2(0, greyNoise.samples() -1));
                greyNoise.loop(1);
                greyNoise.gain(greyNoiseGain);
            }
            if (msg.address == "/pinkNoise") {
                clearAllSound();
                pinkNoise.gain(pinkNoiseGain);
            }
            if (msg.address == "/texture") {
                clearAllSound();
                msg.getInt(0) => int index;
                textures[index].pos(Math.random2(0, textures[index].samples() -1));
                textures[index].loop(1);
                textures[index].gain(textureGain);
            }
            if (msg.address == "/whiteNoiseFadeOut") {
                clearAllSound();
                msg.getFloat(0) => float seconds;
                whiteNoiseFadeOut.gain(whiteNoiseFadeOutGain);
                env.set(1::ms, 0::ms, 0.0, seconds::second);
                env.keyOn();
                samp => now;
                env.keyOff();
            }
            if (msg.address == "/master") {
                msg.getFloat(0) => float gain;
                gain => targetMasterGain;
            }
        }
    }
}


// main proram
// ~-~-

fun void main() {
    spork ~ easeMasterGain();
    clearAllSound();
    oscReceive();
}

main();
