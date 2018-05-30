// desert lines
// receiver script

// written by Eric Heep

// Dog Star 2018
// ~-~-

OscIn in;
OscMsg msg;

// the port for the incoming messages
10001 => in.port;
in.listenAll();

Floors flr;
Wichita wichita;

Gain g => dac;

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            if (msg.address == "/floor") {
                <<< "/floor", msg.getInt(0), msg.getFloat(1) >>>;
                if (msg.getInt(0)) {
                    flr => g;
                    flr.init(msg.getFloat(1));
                    flr.keyOn();
                } else {
                    flr.keyOff();
                    flr =< g;
                }
            }
            if (msg.address == "/wichita") {
                <<< "/wichita", msg.getFloat(0) >>>;
                wichita => g;
                wichita.trigger(msg.getFloat(0));
                wichita =< g;
            }

        }
    }
}

oscReceive();
