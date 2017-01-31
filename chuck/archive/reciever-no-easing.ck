// receiver.ck
// Eric Heep

// osc stuff
OscIn in;
OscMsg msg;

12345 => in.port;
in.listenAll();

// sine tones
SinOsc sin => dac;
sin.gain(0.0);
sin.freq(0.0);
Step st => Gain stGain => dac;

sinGain.gain(0.25);
dac.gain(0.25);

// constant
512 => int bufferSize;
0.0 => float g;

// loop it
while (true) {
    in => now;
    while (in.recv(msg)) {
        // frequency of the sine tone
        if (msg.address == "/sineFreq") {
            msg.getFloat(0) => sin.freq;
            // <<< "/sinFreq", sin.freq() >>>;
        }
        // gain of the sine tone
        if (msg.address == "/sineGain") {
            msg.getFloat(0) => sin.gain;
            // <<< "/sinGain", sin.gain() >>>;
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
