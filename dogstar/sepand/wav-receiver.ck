OscIn in;
OscMsg msg;

// the port for the incoming messages
10001 => in.port;
in.listenAll();

SndBuf wall => Gain g => dac;
wall.loop(1);

fun void changeVolume(float v) {
    g.gain() + v => g.gain;
    if (g.gain() > 1.0) {
        g.gain(1.0);
    }
    if (g.gain() < 0.0) {
        g.gain(0.0);
    }
}

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            <<< msg.address >>>;
            if (msg.address == "/up") {
                changeVolume(0.05);
            }
            if (msg.address == "/down") {
                changeVolume(-0.05);
            }

            if (msg.address == "/wall-one") {
                load("wall-one.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-two") {
                load("wall-two.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-three") {
                load("wall-three.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-four") {
                load("wall-four.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-five") {
                load("wall-five.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-six") {
                load("wall-six.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-seven") {
                load("wall-seven.wav");
                <<< "loaded" >>>;
            }
            if (msg.address == "/wall-eight") {
                load("wall-eight.wav");
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
