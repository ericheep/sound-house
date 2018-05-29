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
            if (msg.address == "/wall-one") load("wall-one.wav");
            if (msg.address == "/wall-two") load("wall-two.wav");
            if (msg.address == "/wall-three") load("wall-three.wav");
            if (msg.address == "/wall-four") load("wall-four.wav");
            if (msg.address == "/wall-five") load("wall-five.wav");
            if (msg.address == "/wall-six") load("wall-six.wav");
            if (msg.address == "/wall-seven") load("wall-seven.wav");
            if (msg.address == "/wall-eight") load("wall-eight.wav");

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
