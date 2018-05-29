[
    "vera.local",
    "ethel.local"
] @=> string IPS[];

[
    "/wall-one",
    "/wall-two",
    "/wall-three",
    "/wall-four",
    "/wall-five",
    "/wall-six",
    "/wall-seven",
    "/wall-eight"
] @=> string addr[];

IPS.size() => int NUM_IPS;

OscOut out[NUM_IPS];
OscMsg msg;

for (0 => int i; i < NUM_IPS; i++) {
    out[i].dest(IPS[i], 10001);
}

second => now;

for (0 => int i; i < NUM_IPS; i++) {
    out[i].start(addr[i]);
    out[i].send();
}

second => now;

for (0 => int i; i < NUM_IPS; i++) {
    out[i].start("/play");
    out[i].send();
}
