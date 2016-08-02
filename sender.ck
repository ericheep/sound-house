// sender.ck
// Eric Heep

// constants
2 => int NUM_PIS;
512 => int BUFFER_SIZE;

// ip addresses
["127.0.0.1",
 "127.0.0.1"] @=> string IP[];

// ports, might as well not change these
[12345,
 12345] @=> int OUT_PORT[];

// not sure if we need to change these either
["/a",
 "/b"] @=> string ADDRESS[];

// osc out
OscOut out[NUM_PIS];

// audio out
Gain mic[NUM_PIS];

// audio set up
for (0 => int i; i < NUM_PIS; i++) {
    adc.chan(i) => mic[i] => blackhole;
    out[i].dest(IP[i], OUT_PORT[i]);
}

// sends out audio in 512 sample blocks
fun void send() {
    for (0 => int i; i < NUM_PIS; i++) {
        out[i].start(ADDRESS[i]);
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

// loop it
while (true) {
    send();
}

