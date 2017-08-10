// audio-test.ck

// Eric Heep

// still not working, will add more later to get it to a good state

/*
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

IP.size() => int NUM_PIS;
7400 => int OUT_PORT;

OscMsg msg;
OscOut out[NUM_PIS];

for (0 => int i; i < NUM_PIS; i++) {
    out[i].dest(IP[i], OUT_PORT);
}

while(true) {
    for (0 => int i; i < NUM_PIS; i++) {
        out[i].start("/sineGain");
        out[i].add(1.0);
        out[i].send();

        1::ms => now;

        out[i].start("/sineFreq");
        out[i].add(400);
        out[i].send();

        0.5::second => now;

        out[i].start("/sineGain");
        out[i].add(0.0);
        out[i].send();

        1::ms => now;
        <<< "pi", i + 1, "" >>>;
    }
}
*/

OscOut out;
OscMsg msg;

out.dest("127.0.0.1", 7400);

out.start("/threshold" + 3);
out.add(10.0);
out.send();
