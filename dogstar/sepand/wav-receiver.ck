OscIn in;
OscMsg msg;

// the port for the incoming messages
10001 => in.port;
in.listenAll();

SndBuf leftChannel => dac;
SndBuf rightChannel => dac;

leftChannel.read(me.dir() + "left-channel.wav");
leftChannel.gain(0.5);
leftChannel.pos(leftChannel.samples() - 1);

rightChannel.read(me.dir() + "right-channel.wav");
rightChannel.gain(0.5);
rightChannel.pos(rightChannel.samples() - 1);

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            if (msg.address == "/left-channel") {
                leftChannel.pos(0);
            }
            if (msg.address == "/right-channel") {
                rightChannel.pos(0);
            }
        }
    }
}

spork ~ oscReceive();

while (second => now) {}
