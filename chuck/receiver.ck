// receiver.ck
// Eric Heep

// osc stuff
OscIn in;
OscMsg msg;
Step st => ADSR env => dac;

128::samp => dur attackTime;
128::samp => dur releaseTime;
env.set(attackTime, 0::samp, 1.0, releaseTime);

// constant
512 => int bufferSize;

12345 => in.port;
in.listenAll();

fun void envelope() {
    env.keyOn();
    attackTime => now;
    (bufferSize::samp) - releaseTime => now;
    env.keyOff();
}

// loop it
while (true) {
    in => now;
    while (in.recv(msg)) {
        if (msg.address == "/m") {
            spork ~ envelope();
            for (0 => int i; i < bufferSize; i++) {
                msg.getFloat(i) => st.next;
                1::samp => now;
            }
        }
        else if (msg.address == "/bufferSize") {
            msg.getInt(0) => bufferSize;
            <<< "Buffer size set to", bufferSize, "" >>>;
        }
    }
}
