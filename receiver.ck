OscIn in;
OscMsg msg;
Step st => dac;

512 => int BUFFER_SIZE;

12345 => in.port;
in.listenAll();

while (true) {
    in => now;
    while (in.recv(msg)) {
        if (msg.address == "/a") {
            for (0 => int i; i < BUFFER_SIZE; i++) {
                msg.getFloat(i) => st.next;
                1::samp => now;
            }
        }
    }
}
