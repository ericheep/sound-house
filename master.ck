// master.ck
// Eric Heep

// constants
1 => int NUM_PIS;
512 => int BUFFER_SIZE;

string ip[NUM_PIS];
int OUT_PORT;

// osc out
OscOut out
out.dest(ip, outPort);

// set parameters

float buffer[NUM_PIS][0];

SinOsc sin => dac;

fun void send() {
    for (0 => int i; i < NUM_PIS; i++) {
        for (0 => int j; j < BUFFER_SIZE; i++) {

        }
    }
}

while (true) {

}

