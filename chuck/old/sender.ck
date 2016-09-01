// sender.ck
// Eric Heep

// constants
1 => int NUM_PIS;
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
12345 => int OUT_PORT;

// address is the same for all
"/m" => string ADDRESS;

// we'll try this out
100::ms => dur delayTime;

// osc out
OscOut out[NUM_PIS];

// UGens
Gain mic[NUM_PIS];
Delay del[NUM_PIS];
OnePole pole[NUM_PIS];

// thresholds in decibels
15.0 => float risingThreshold;
1.0 => float fallingThreshold;

400::ms => dur minimumLength;

// set up
for (0 => int i; i < NUM_PIS; i++) {
    // sound chain
    adc.chan(i) => mic[i] => del[i] => blackhole;
    mic[i] => pole[i] => blackhole;
    // delay stuff
    del[i].max(delayTime);
    del[i].delay(delayTime);
    // osc stuff
    out[i].dest(IP[i], OUT_PORT);
    // following
    3 => pole[i].op;
    0.9999 => pole[i].pole;
    spork ~ envelopeFollower(i);
}

fun void envelopeFollower(int idx) {
    // loops until the decibel limit is reached
    while (true) {
        while (Std.rmstodb(pole[idx].last()) < risingThreshold) {
            1::samp => now;
        }
        <<< "Sending!", Std.rmstodb(pole[idx].last()) >>>;
        now => time past;
        while (Std.rmstodb(pole[idx].last()) > fallingThreshold
            ||  now < past + minimumLength) {
            send();
            //1024::samp => now;
        }
        <<< "Sent!", Std.rmstodb(pole[idx].last()) >>>;
    }
}

// sends out audio in 512 sample blocks
fun void send() {
    for (0 => int i; i < NUM_PIS; i++) {
        out[i].start(ADDRESS);
    }

    for (0 => int j; j < BUFFER_SIZE; j++) {
        for (0 => int i; i < NUM_PIS; i++) {
            out[i].add(del[i].last());
        }
        // for 22050 on the other end
        2::samp => now;
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
    // send();
    1::ms => now;
}

