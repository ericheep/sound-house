// sender.ck
// Eric Heep

/*
sine tone freq per pi
sine tone gain per pi

mic volume per pi
lookback delay time per pi
packet length per pi
threshold per pi

cutoff freq per pi
resonance Q per pi
envelope length
*/

// constants
512 => int BUFFER_SIZE;

// --------------------------------------------------------------
// osc out ------------------------------------------------------
// --------------------------------------------------------------

// ip addresses
[
 "pione.local",
 "pitwo.local",
 "pithree.local",
 "pifour.local",
 "pifive.local",
 "pisix.local",
 "piseven.local",
 "pieight.local"
] @=> string IP[];

IP.size() => int NUM_IPS;

8 => int NUM_PIS;

// port is the same for all outgoing messages
10001 => int OUT_PORT;

// address is the same for all outgoing messages
"/m" => string ADDRESS;

// osc out to Raspberry Pis
OscOut out[NUM_PIS];

// determines our packet length for outgoing messages
dur packetLength[NUM_PIS];

// --------------------------------------------------------------
// osc in -------------------------------------------------------
// --------------------------------------------------------------

OscIn in;
OscMsg msg;

// the port for the incoming messages
7400 => in.port;
in.listenAll();

// --------------------------------------------------------------
// microphone audio ---------------------------------------------
// --------------------------------------------------------------

Gain mic;
Gain gain[NUM_PIS];
HPF hp[NUM_PIS];
LPF lp[NUM_PIS];
ResonZ res[NUM_PIS];
Delay del[NUM_PIS];
OnePole pole[NUM_PIS];

// we'll try this out
dur delayLength[NUM_PIS];
float threshold[NUM_PIS];

// --------------------------------------------------------------
// initialize ---------------------------------------------------
// --------------------------------------------------------------

adc => mic;
for (0 => int i; i < NUM_PIS; i++) {
    // sound chain
    //mic => gain[i] => res[i] => lp[i] => hp[i] => del[i] => blackhole;
    mic => gain[i] => lp[i] => hp[i] => del[i] => blackhole;
    //mic => gain[i] => del[i] => blackhole;
    mic => pole[i] => blackhole;

    // delay of adc
    100::ms => delayLength[i];

    // delay stuff
    del[i].max(100::ms);
    del[i].delay(100::ms);

    hp[i].freq(0.1);
    lp[i].freq(10000.0);

    // following
    3 => pole[i].op;
    0.9999 => pole[i].pole;

    // thresholds in decibels
    10 => threshold[i];

    // this determines how much audio is send through in milliseconds
    500::ms => packetLength[i];
}

for (0 => int i; i < NUM_IPS; i++) {
    // start the envelope follower
    spork ~ envelopeFollower(i);

     // set ip and port for each osc out
    out[i].dest(IP[i], OUT_PORT);

    // set buffer_size
    out[i].start("/bufferSize");
    out[i].add(BUFFER_SIZE);
    out[i].send();

}

// allows Max/MSP to change the values of
// the threshold and length variables
fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            for (int i; i < NUM_PIS; i++) {
                if (msg.address == "/hpCutoff" + i) {
                    msg.getFloat(0) => float hpFreq;
                    Std.clampf(hpFreq, 0.1, 22050.0) => hp[i].freq;
                    <<< "/hpCutoff" + i, hp[i].freq(), "" >>>;
                }
                if (msg.address == "/lpCutoff" + i) {
                    msg.getFloat(0) => float lpFreq;
                    Std.clampf(lpFreq, 0.1, 22050.0) => lp[i].freq;
                    <<< "/lpCutoff" + i, lp[i].freq(), "" >>>;
                }
                if (msg.address == "/res" + i) {
                    msg.getFloat(0) => res[i].Q;
                    <<< "/res" + i, res[i].Q(), "" >>>;
                }
                if (msg.address == "/packetLength" + i) {
                    msg.getFloat(0)::ms => packetLength[i];
                    <<< "/packetLength" + i, packetLength[i]/ms, "" >>>;
                }
                if (msg.address == "/threshold" + i) {
                    msg.getFloat(0) => threshold[i];
                    <<< "/threshold" + i, threshold[i], "" >>>;
                }
                if (msg.address == "/micGain" + i) {
                    msg.getFloat(0) => gain[i].gain;
                    <<< "/micGain" + i, gain[i].gain(), "" >>>;
                }
                if (msg.address == "/delayLength" + i) {
                    msg.getFloat(0)::ms => delayLength[i];
                    <<< "/delayLength" + i, delayLength[i]/ms, "" >>>;
                }
            }
        }
    }
}

spork ~ oscReceive();

// envelope follower
fun void envelopeFollower(int idx) {
    // loops until the decibel limit is reached
    while (true) {
        while (Std.rmstodb(pole[idx].last()) < threshold[idx]) {
            1::samp => now;
        }
        <<< "Sound.", "" >>>;

        send(idx);
        now => time past;

        while (now < past + packetLength[idx]) {
            send(idx);
        }
    }
}

// sends out audio in 512 sample blocks
fun void send(int idx) {
    out[idx].start(ADDRESS);

    for (0 => int j; j < BUFFER_SIZE; j++) {
        out[idx].add(del[idx].last());
        1::samp => now;
    }

    out[idx].send();
}

// loop it
while (true) {
    1::ms => now;
}
