// sender.ck
// Eric Heep

// constants
5 => int NUM_PIS;
512 => int BUFFER_SIZE;

// ip addresses
["192.168.1.11",
 "192.168.1.12",
 "192.168.1.13",
// "192.168.1.14",
// "192.168.1.15",
 "192.168.1.16",
 "192.168.1.17"
// "192.168.1.18"
] @=> string IP[];

// port is the same for all
12345 => int OUT_PORT;

// address is the same for all
"/m" => string ADDRESS;

// we'll try this out
100::ms => dur delayTime;

// osc out
OscOut out[NUM_PIS];

// UGens
Gain mic;
Delay del;
OnePole pole;

// thresholds in decibels
15.0 => float risingThreshold;
1.0 => float fallingThreshold;

400::ms => dur minimumLength;

for (0 => int i; i < NUM_PIS; i++) {
    out[i].dest(IP[i], OUT_PORT);
}

// sound chain
adc => mic => del => blackhole;
mic => pole => blackhole;
// delay stuff
del.max(delayTime);
del.delay(delayTime);
// osc stuff
3 => pole.op;
0.9999 => pole.pole;
spork ~ envelopeFollower();

fun void envelopeFollower() {
    // loops until the decibel limit is reached
    while (true) {
        while (Std.rmstodb(pole.last()) < risingThreshold) {
            1::samp => now;
        }
        Math.random2(0, IP.cap()) => int choice;
        <<< "Sending!", Std.rmstodb(pole.last()), choice >>>;
        now => time past;
        while (Std.rmstodb(pole.last()) > fallingThreshold
            ||  now < past + minimumLength) {
            send(choice);
            //1024::samp => now;
        }
        <<< "Sent!", Std.rmstodb(pole.last()) >>>;
    }
}

// sends out audio in 512 sample blocks
fun void send(int idx) {
    for (0 => int i; i < NUM_PIS; i++) {
        out[i].start(ADDRESS);
    }

    for (0 => int j; j < BUFFER_SIZE; j++) {
        for (0 => int i; i < NUM_PIS; i++) {
            out[i].add(del.last());
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

