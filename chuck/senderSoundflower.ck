// sender.ck
// Eric Heep

// constants
512 => int BUFFER_SIZE;

// ip addresses
[
 "192.168.1.11",
 "192.168.1.12",
 "192.168.1.13",
 "192.168.1.14",
 "192.168.1.15",
 "192.168.1.16",
 "192.168.1.17",
 "192.168.1.18"
] @=> string IP[];

IP.cap() => int NUM_PIS;

// port is the same for all outgoing messages
12345 => int OUT_PORT;

// address is the same for all outgoing messages
"/m" => string ADDRESS;

// we'll try this out
100::ms => dur delayTime;

// osc out to Raspberry Pis
OscOut out[NUM_PIS];
// osc in to ChucK from Max

OscIn in;
OscMsg msg;

// the port for the incoming messages
7400 => in.port;
in.listenAll();

// UGens
Gain mic[NUM_PIS];
Delay del[NUM_PIS];
OnePole pole[NUM_PIS];

// thresholds in decibels
10 => int risingThreshold;  //10
1 => int fallingThreshold;

// this determines how much audio is send through in milliseconds
400::ms => dur packetLength;  //10


// allows Max/MSP to change the values of
// the threshold and length variables
fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            if (msg.address == "/risingThreshold") {
                <<< msg.getInt(0), "rising" >>>;
                //msg.getInt(0) => risingThreshold;
            }
            if (msg.address == "/fallingThreshold") {
                                <<< msg.getInt(0), "Falling" >>>;

                //msg.getInt(0) => fallingThreshold;
            }
            if (msg.address == "/packetLength") {
                //msg.getInt(0)::ms => packetLength;
            }
            if (msg.address == "/delayTime") {
                //msg.getInt(0)::ms => delayTime;
            }
<<<<<<< HEAD
         }
         //1::ms => now;
=======
            <<<"Rising", risingThreshold, "Falling", fallingThreshold,
            "Packet Length", packetLength/ms, "Delay Time", delayTime/ms >>>;
        }
        1::ms => now;
>>>>>>> 2670b9960465164c062754accad70df6176db185
    }
}

spork ~ oscReceive();

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

// envelope follower
fun void envelopeFollower(int idx) {
    // loops until the decibel limit is reached
    while (true) {
        while (Std.rmstodb(pole[idx].last()) < risingThreshold) {
            1::samp => now;
        }
        <<< "Sending!", Std.rmstodb(pole[idx].last()), risingThreshold >>>;
        now => time past;
<<<<<<< HEAD
        //while (Std.rmstodb(pole[idx].last()) > fallingThreshold
        //    ||  now < past + packetLength) {
=======
        // while (Std.rmstodb(pole[idx].last()) > fallingThreshold ||  now < past + packetLength) {
>>>>>>> 2670b9960465164c062754accad70df6176db185
        while (now < past + packetLength) {
            send(idx);
            //1024::samp => now;
        }
        <<< "Sent!", Std.rmstodb(pole[idx].last()) >>>;
    }
}

// sends out audio in 512 sample blocks
fun void send(int idx) {
    out[idx].start(ADDRESS);

    for (0 => int j; j < BUFFER_SIZE; j++) {
        out[idx].add(del[idx].last());
        // for 22050 on the other end
        2::samp => now;
    }

    out[idx].send();
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
    // <<< Std.rmstodb(pole[0].last()) >>>;
    // <<< "!" >>>;
    100::ms => now;
}

