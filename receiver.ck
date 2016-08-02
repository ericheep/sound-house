// receiver.ck
// Eric Heep

OscIn in;
OscMsg msg;
Step st => dac;

// constant
512 => int bufferSize;

12345 => in.port;
in.listenAll();

// loop it
while (true) {
    in => now;
    while (in.recv(msg)) {
        if (msg.address == "/b") {
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
