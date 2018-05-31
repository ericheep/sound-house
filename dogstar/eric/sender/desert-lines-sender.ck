// desert lines
// sender script

// written by Eric Heep
// Dog Star 2018
// ~-~-

/* [ */
/*     "pione.local", "pitwo.local", "pithree.local", "pifour.local", */
/*     "pifive.local", "pisix.local", "piseven.local", "pieight.local" */
/* ] @=> string hostnames[]; */

[ "liafd.local" ] @=> string hostnames[];

UltrasonicHandler uh;
uh.init(hostnames, 5000, 12345);

PiHandler ph;
ph.init(hostnames, 10001);

while (true) {
    uh.passingEvent => now;
    <<< uh.passingEvent.value, uh.passingEvent.reading >>>;
}
