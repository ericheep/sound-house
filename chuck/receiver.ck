// receiver.ck
// Eric Heep

// osc stuff
OscIn in;
OscMsg msg;

[
 me.dir(-1) + "samples/fake-bricks/fake-brick-1.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-2.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-3.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-4.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-5.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-6.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-7.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-8.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-9.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-10.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-11.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-12.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-13.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-14.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-15.wav",
 me.dir(-1) + "samples/fake-bricks/fake-brick-16.wav"
] @=> string brickSamplePaths[];

brickSamplePaths.size() => int numBrickSamples;

SndBuf brickSamples[numBrickSamples];

for (0 => int i; i < numBrickSamples; i++) {
    brickSamples[i] => dac;
    brickSamples[i].read(brickSamplePaths[i]);
    brickSamples[i].pos(brickSamples[i].samples());
}

10001 => in.port;
in.listenAll();

// sine tones
SinOsc sin => dac;
sin.gain(0.0);
sin.freq(1.0);

Step st => Gain stGain => dac;

// because of distortion
dac.gain(0.5);

0.001 => float gainInc;
0.0 => float targetGain;

fun void easeGain() {
    while (true) {
        if (sin.gain() < targetGain - gainInc) {
	    sin.gain() + gainInc => sin.gain;
        }
        else if (sin.gain() > targetGain + gainInc) {
            sin.gain() - gainInc => sin.gain;
        }
        1::ms => now;
    }
}

spork ~ easeGain();

// constant
512 => int bufferSize;

// loop it
while (true) {
    in => now;
    while (in.recv(msg)) {
        // frequency of the sine tone
        if (msg.address == "/sineFreq") {
            msg.getFloat(0) => sin.freq;
            <<< "/sineFreq", sin.freq() >>>;
        }
        // gain of the sine tone
        if (msg.address == "/sineGain") {
            msg.getFloat(0) => targetGain;
            <<< "/sineGain", targetGain >>>;
        }
        // receive packet of audio samples
        if (msg.address == "/m") {
            <<< "received sound", "" >>>;
            stGain.gain(1.0);
            // start the sample playback
            for (0 => int i; i < bufferSize; i++) {
                msg.getFloat(i) => st.next;
                1::samp => now;
            }

            stGain.gain(0.0);

        }
        if (msg.address == "/bufferSize") {
            msg.getInt(0) => bufferSize;
            <<< "Buffer size set to", bufferSize, "" >>>;
        }
        if (msg.address == "/brickPlay") {
            msg.getInt(0) => int idx;
            if (idx > 0 && idx < numBrickSamples) {
                brickSamples[idx].pos(0);
            }
        }
    }
    1::samp => now;
}
