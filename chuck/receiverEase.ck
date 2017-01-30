// receiver.ck
// Eric Heep

// osc stuff
OscIn in;
OscMsg msg;

12345 => in.port;
in.listenAll();

// sine tones
SinOsc sin => Gain sinGain => dac;
sin.gain(0.00001);
sin.freq(1.0);
sinGain.gain(0.0);

Step st => Gain stGain => dac;

0.001 => float gainInc;
0.0 => float targetGain;

fun void easeGain() {
    while (true) {
        if (sinGain.gain() < targetGain - gainInc) {
	    sinGain.gain() + gainInc => sinGain.gain;
            <<< sinGain.gain() >>>;
	}     
        else if (sinGain.gain() > targetGain + gainInc) {
            sinGain.gain() - gainInc => sinGain.gain;
            <<< sinGain.gain() >>>;
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
            <<< "/sinFreq", sin.freq() >>>;
        }
        // gain of the sine tone
        if (msg.address == "/sinGain") {
            msg.getFloat(0) => targetGain;
            // <<< "/sinGain", targetGain >>>;
        }
        // receive packet of audio samples
        if (msg.address == "/m") {
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
    }
    1::samp => now;
}
