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
Bumps bumps;
NoiseTones noiseTones;
GasStation gasStation;
Freezer freezer;

int flrConnected;
int wichitaConnected;
int bumpsConnected;
int noiseTonesConnected;
int gasStationConnected;
int freezerConnected;

Gain g => dac;

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            if (msg.address == "/floor") {
                <<< "/floor", msg.getInt(0), msg.getFloat(1) >>>;
                if (msg.getInt(0)) {
                    if (flrConnected == 0) {
                        flr => g;
                        1 => flrConnected;
                    }
                    flr.init(msg.getFloat(1));
                    flr.keyOn();
                } else {
                    flr.keyOff();
                    if (flrConnected == 1) {
                        flr =< g;
                        0 => flrConnected;
                    }
                }
            }
            if (msg.address == "/wichita") {
                <<< "/wichita", msg.getFloat(0) >>>;
                if (wichitaConnected == 0) {
                    wichita => g;
                    1 => wichitaConnected;
                }
                wichita.trigger(msg.getFloat(0));
                if (wichitaConnected == 1) {
                    wichita =< g;
                    0 => wichitaConnected;
                }
            }
            if (msg.address == "/bumps") {
                <<< "/bumps", msg.getFloat(0) >>>;
                if (bumpsConnected == 0) {
                    bumps => g;
                    1 => bumpsConnected;
                }
                bumps.trigger(msg.getFloat(0));
                if (bumpsConnected == 1) {
                    bumps =< g;
                    0 => bumpsConnected;
                }
            }
            if (msg.address == "/noiseTones") {
                <<< "/noiseTones", msg.getFloat(0) >>>;
                if (noiseTonesConnected == 0) {
                    noiseTones => g;
                    0 => noiseTonesConnected;
                }
                noiseTones.trigger(msg.getFloat(0));
                if (noiseTonesConnected == 1) {
                    noiseTones =< g;
                    1 => noiseTonesConnected;
                }
            }
            if (msg.address == "/gasStation") {
                <<< "/gasStation", msg.getFloat(0) >>>;
                if (gasStationConnected == 0) {
                    gasStation => g;
                    0 => gasStationConnected;
                }
                gasStation.trigger(msg.getFloat(0));
                if (gasStationConnected == 1) {
                    gasStation =< g;
                    1 => gasStationConnected;
                }
            }
            if (msg.address == "/freezer") {
                <<< "/freezer", msg.getFloat(0) >>>;
                if (freezerConnected == 0) {
                    freezer => g;
                    0 => freezerConnected;
                }
                freezer.trigger(msg.getFloat(0));
                if (freezerConnected == 1) {
                    freezer =< g;
                    1 => freezerConnected;
                }
            }
        }
    }
}

oscReceive();
