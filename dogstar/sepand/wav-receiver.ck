OscIn in;
OscMsg msg;

// the port for the incoming messages
10001 => in.port;
in.listenAll();

SndBuf wall => dac;

wall.gain(0.8);

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            if (msg.address == "/wall-one") {
                load("FirstPairLeft.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-two") {
                load("FirstPairRight.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-three") {
                load("SecondPairLeft.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-four") {
                load("SecondPairRight.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-five") {
                load("ThirdPairLeft.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-six") {
                load("ThirdPairRight.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-seven") {
                load("FourthPairLeft.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-eight") {
                load("FourthPairRight.wav");
                <<< "loaded" >>>;
            }

            if (msg.address == "/play") {
                wall.pos(0);
            }
        }
    }
}

fun void load(string filename) {
    wall.read(me.dir() + "/wavs/" + filename);
    wall.pos(wall.samples() - 1);
}

spork ~ oscReceive();

while (second => now) {}
