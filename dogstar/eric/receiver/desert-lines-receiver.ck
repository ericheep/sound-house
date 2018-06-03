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
gasStation.gain(0.2);

Microwave microwave => g;
microwave.gain(0.1);

Freezer freezer => g;
freezer.gain(0.1);

Wichita1 wichita1 => g;
wichita1.gain(0.2);

Wichita2 wichita2 => g;
wichita2.gain(0.2);

Stone1 stone1 => g;
stone1.gain(1.0);

Stone2 stone2 => g;
stone2.gain(1.0);

Traffic traffic => g;
traffic.gain(1.0);

Fades fades => g;
fades.gain(0.5);

Beeps beeps => g;
beeps.gain(0.3);

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
            if (msg.address == "/microwave") {
                if (!microwave.isRunning()) {
                    spork ~ microwave.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/beeps") {
                if (!beeps.isRunning()) {
                    spork ~ beeps.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/fades") {
                if (!fades.isRunning()) {
                    spork ~ fades.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/freezer") {
                if (!freezer.isRunning()) {
                    spork ~ freezer.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/wichita1") {
                if (!wichita1.isRunning()) {
                    spork ~ wichita1.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/wichita2") {
                if (!wichita2.isRunning()) {
                    spork ~ wichita2.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/stone1") {
                if (!stone1.isRunning()) {
                    spork ~ stone1.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/stone2") {
                if (!stone2.isRunning()) {
                    spork ~ stone2.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/traffic") {
                if (!traffic.isRunning()) {
                    spork ~ traffic.trigger(msg.getFloat(0));
                }
            }
            if (msg.address == "/end") {
                g.gain(0.0);
            }
        }
    }
}

oscReceive();
