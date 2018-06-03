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
Bumps bumps => g;
NoiseTones noiseTones => g;
GasStation gasStation => g;
Microwave microwave => g;
Freezer freezer => g;
Wichita1 wichita1 => g;
Wichita2 wichita2 => g;
Stone1 stone1 => g;
Stone2 stone2 => g;
Traffic traffic => g;
Fades fades => g;
Beeps beeps => g;

fun void oscReceive() {
    while (true) {
        in => now;
        while (in.recv(msg)) {
            <<< msg.address, msg.getFloat(0) >>>;
            if (msg.address == "/floor") {
                if (!floor.isRunning()) {
                    spork ~ floor.trigger(msg.getFloat(0));
                    floor.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/bumps") {
                if (!bumps.isRunning()) {
                    spork ~ bumps.trigger(msg.getFloat(0));
                    bumps.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/noiseTones") {
                if (!noiseTones.isRunning()) {
                    spork ~ noiseTones.trigger(msg.getFloat(0));
                    noiseTones.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/gasStation") {
                if (!gasStation.isRunning()) {
                    spork ~ gasStation.trigger(msg.getFloat(0));
                    gasStation.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/microwave") {
                if (!microwave.isRunning()) {
                    spork ~ microwave.trigger(msg.getFloat(0));
                    microwave.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/beeps") {
                if (!beeps.isRunning()) {
                    spork ~ beeps.trigger(msg.getFloat(0));
                    beeps.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/fades") {
                if (!fades.isRunning()) {
                    spork ~ fades.trigger(msg.getFloat(0));
                    fades.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/freezer") {
                if (!freezer.isRunning()) {
                    spork ~ freezer.trigger(msg.getFloat(0));
                    freezer.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/wichita1") {
                if (!wichita1.isRunning()) {
                    spork ~ wichita1.trigger(msg.getFloat(0));
                    wichita1.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/wichita2") {
                if (!wichita2.isRunning()) {
                    spork ~ wichita2.trigger(msg.getFloat(0));
                    wichita2.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/stone1") {
                if (!stone1.isRunning()) {
                    spork ~ stone1.trigger(msg.getFloat(0));
                    stone1.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/stone2") {
                if (!stone2.isRunning()) {
                    spork ~ stone2.trigger(msg.getFloat(0));
                    stone2.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/traffic") {
                if (!traffic.isRunning()) {
                    spork ~ traffic.trigger(msg.getFloat(0));
                    traffic.gain(msg.getFloat(1));
                }
            }
            if (msg.address == "/end") {
                g.gain(0.0);
            }
        }
    }
}

oscReceive();
