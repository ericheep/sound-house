// test-receiver.ck
// Eric Heep

OscIn in;
OscMsg msg;

OscOut out;
out.dest("pieight.local", 5000);

12345 => in.port;
in.listenAll();

fun void sendWall() {
    while (true) {
        out.start("/w");
        out.send();
        100::ms => now;
    }
}

spork ~ sendWall();

// loop it
while (true) {
    in => now;
    while (in.recv(msg)) {
        // frequency of the sine tone
        if (msg.address == "/w") {
            <<< msg.getString(0), msg.getFloat(1) >>>;
        }
    }
    1::samp => now;
}
