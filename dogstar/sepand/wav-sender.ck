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


Hid hi;
HidMsg hidMsg;

[49, 50, 51, 52, 53, 54, 55, 56] @=> int topRow[];
[81, 87, 69, 82, 84, 89, 85, 73] @=> int bottomRow[];

80 => int play;

// which keyboard
0 => int device;
// get from command line
if( me.args() ) me.arg(0) => Std.atoi => device;

// open keyboard (get device number from command line)
if( !hi.openKeyboard( device ) ) me.exit();
<<< "keyboard '" + hi.name() + "' ready", "" >>>;

while( true ) {
    hi => now;

    while( hi.recv( hidMsg ) ) {
        if( hidMsg.isButtonDown() ) {
            for (0 => int i; i < topRow.size(); i++) {
                if (hidMsg.ascii == topRow[i]) {
                    out[i].start("/up");
                    out[i].send();
                }
                if (hidMsg.ascii == bottomRow[i]) {
                    out[i].start("/down");
                    out[i].send();
                }
            }

            if (hidMsg.ascii == play) {
                for (0 => int i; i < NUM_IPS; i++) {
                    out[i].start("/play");
                    out[i].send();
                }
            }
        }
    }
}
