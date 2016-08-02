// sender.ck
// Eric Heep

// constants
1 => int NUM_PIS;
512 => int BUFFER_SIZE;

["127.0.0.1"] @=> string IP[];
[12345] @=> int OUT_PORT[];
["/a"] @=> string ADDRESS[];

// osc out
OscOut out[NUM_PIS];

// audio out
SinOsc sin[NUM_PIS];

for (0 => int i; i < NUM_PIS; i++) {
    out[i].dest(IP[i], OUT_PORT[i]);
    sin[i].freq(220 * (i + 1));
}

// container for all our samples
float buffer[NUM_PIS][BUFFER_SIZE];

fun void collect() {
    for (0 => int j; j < BUFFER_SIZE; j++) {
        for (0 => int i; i < NUM_PIS; i++) {
            sin[i].last() => buffer[i][j];
        }
        1::samp => now;
    }
}

fun void send() {
    for (0 => int i; i < NUM_PIS; i++) {
        out[i].start(ADDRESS[i]);
    }

    for (0 => int j; j < BUFFER_SIZE; j++) {
        for (0 => int i; i < NUM_PIS; i++) {
            out[i].add(sin[i].last());
            // sin[i].last() => buffer[i][j];
        }
        1::samp => now;
    }

    for (0 => int i; i < NUM_PIS; i++) {
        out[i].send();
    }
}

while (true) {
    send();
}

