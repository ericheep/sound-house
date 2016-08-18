// sender.ck
// Eric Heep

// constants
8 => int NUM_PIS;
512 => int BUFFER_SIZE;

// ip addresses
["192.168.1.11",
 "192.168.1.12",
 "192.168.1.13",
 "192.168.1.14",
 "192.168.1.15",
 "192.168.1.16",
 "192.168.1.17",
 "192.168.1.18"] @=> string IP[];

// port is the same for all
12345 => int OUT_PORT[];

// address is the same for all
"/m" => string ADDRESS[];

// osc out
OscOut out[NUM_PIS];

// audio out
Gain mic[NUM_PIS];

// audio set up
for (0 => int i; i < NUM_PIS; i++) {
    adc.chan(i) => mic[i] => blackhole;
    out[i].dest(IP[i], OUT_PORT);
}

// sends out audio in 512 sample blocks
fun void send() {
    for (0 => int i; i < NUM_PIS; i++) {
        out[i].start(ADDRESS);
    }

    for (0 => int j; j < BUFFER_SIZE; j++) {
        for (0 => int i; i < NUM_PIS; i++) {
            out[i].add(mic[i].last());
        }
        1::samp => now;
    }

    for (0 => int i; i < NUM_PIS; i++) {
        out[i].send();
    }
}

fun void init() {
    for (0 => int i; i < NUM_PIS; i++) {
        out[i].start("/bufferSize");
        out[i].add(BUFFER_SIZE);
        out[i].send();
    }
}

// updates buffer size
init();

// loop it
while (true) {
    send();
}

