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
Step st => ADSR env => dac;

// envelope
0.0 => float win;
0::samp => dur winDur;
env.set(winDur, 0::samp, 1.0, winDur);

// constant
512 => int bufferSize;

// run concurrently with sample playback
fun void envelope() {
    env.keyOn();
    winDur => now;
    (bufferSize::samp) - winDur => now;
    env.keyOff();
}

// loop it
while (true) {
    in => now;
    while (in.recv(msg)) {
        // frequency of the sine tone
        if (msg.address == "/sineFreq") {
            msg.getFloat(0) => sin.freq;
        }
        // gain of the sine tone
        if (msg.address == "/sineGain") {
            msg.getFloat(0) => sin.gain;
        }
        // receive envelope length
        if (msg.address == "/envLength") {
            msg.getFloat(0) => win;
        }
        // receive packet of audio samples
        if (msg.address == "/m") {
            (win * 0.5 * bufferSize)::samp => winDur;
            env.set(winDur, 0::samp, 1.0, winDur);

            // start envelope
            spork ~ envelope();

            // start the sample playback
            for (0 => int i; i < bufferSize; i++) {
                msg.getFloat(i) => st.next;
                1::samp => now;
            }
        }
        if (msg.address == "/bufferSize") {
            msg.getInt(0) => bufferSize;
            <<< "Buffer size set to", bufferSize, "" >>>;
        }
    }
}
