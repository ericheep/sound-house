[
    "vera.local",
    "liafd.local",
] @=> string IPS[];

IPS.size() => NUM_IPS;

OscOut out[NUM_IPS];
OscMsg msg;

for (0 => int i; i < NUM_IPS; i++) {
    out[i].dest(IPS[i], OUT_PORT);
}

5::second => now;

out[0].start("/left-channel");
out[0].send();
out[1].start("/right-channel");
out[1].send();

1::second => now;
