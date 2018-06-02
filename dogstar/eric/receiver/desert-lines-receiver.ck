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

Gain g => dac;

Floors floor => g;
floor.gain(1.0);

Bumps bumps => g;
bumps.gain(1.0);

NoiseTones noiseTones => g;
noiseTones.gain(0.02);

GasStation gasStation => g;
gasStation.gain(0.3);

Freezer freezer => g;
freezer.gain(0.1);

Wichita wichita => g;
wichita.gain(1.0);

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            <<< msg.address, msg.getFloat(0) >>>;
            if (msg.address == "/floor") {
                if (!floor.isRunning()) {
                    spork ~ floor.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/bumps") {
                if (!bumps.isRunning()) {
                    spork ~ bumps.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/noiseTones") {
                if (!noiseTones.isRunning()) {
                    spork ~ noiseTones.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/gasStation") {
                if (!gasStation.isRunning()) {
                    spork ~ gasStation.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/freezer") {
                if (!freezer.isRunning()) {
                    spork ~ freezer.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/wichita") {
                if (!wichita.isRunning()) {
                    spork ~ wichita.trigger(msg.getFloat(0));
                }
            }
            /*
            if (msg.address == "/wichita") {
                <<< "/wichita", msg.getFloat(0) >>>;
                if (wichitaConnected == 0) {
                    wichita => g;
                    1 => wichitaConnected;
                    spork ~ wichita.trigger(msg.getFloat(0));
                }
                if (wichitaConnected == 1) {
                    wichita =< g;
                    0 => wichitaConnected;
                }
            }
            if (msg.address == "/gasStation") {
                <<< "/gasStation", msg.getFloat(0) >>>;
                if (gasStationConnected == 0) {
                    gasStation => g;
                    1 => gasStationConnected;
                    spork ~ gasStation.trigger(msg.getFloat(0));
                }
                if (gasStationConnected == 1) {
                    gasStation =< g;
                    0 => gasStationConnected;
                }
            }
            if (msg.address == "/freezer") {
                <<< "/freezer", msg.getFloat(0) >>>;
                if (freezerConnected == 0) {
                    1 => freezerConnected;
                    freezer => g;
                    spork ~ freezer.trigger(msg.getFloat(0));
                }
                if (freezerConnected == 1) {
                    freezer =< g;
                    0 => freezerConnected;
                }
            }*/
        }
    }
}

oscReceive();
