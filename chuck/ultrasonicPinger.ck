8 => int NUM_PIS;
5000 => int OUT_PORT;

OscOut out[NUM_PIS];
OscIn in;
OscMsg msg;

["192.168.1.11",
 "192.168.1.12",
 "192.168.1.13",
 "192.168.1.14",
 "192.168.1.15",
 "192.168.1.16",
 "192.168.1.17",
 "192.168.1.18"] @=> string ips[];

for (0 => int i; i < NUM_PIS; i++) {
    out[i].dest(ips[i], OUT_PORT);
}

float incMsg[NUM_PIS];

in.port(12345);
in.listenAll();

spork ~ oscOut();
// spork ~ oscIn();

// max out around 0.2 seconds
fun void oscOut() {
    while (true) {
        for (0 => int i; i < NUM_PIS; i++) {
            out[i].start("/wait");
            out[i].add(0);
            out[i].send();
            0.02::second => now;
        }
    }
}

fun void oscIn() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            for (0 => int i; i < NUM_PIS; i++) {
                if (msg.address == "/" + ips[i]) {
                    msg.getFloat(0) => incMsg[i];
                }
            }
        }
    }
}

while (true) {
    "" => string print;
    for (0 => int i; i < NUM_PIS; i++) {
        print + Math.round(incMsg[i]) + " "  => print;
    }
    // <<< print, "" >>>;
    0.5::second => now;
}
