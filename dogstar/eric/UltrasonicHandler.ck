// UltrasonicHandler
// written by Eric heep

// Dog Star 2018
// ~-~-

public class UltrasonicHandler {



    [
        "pione.local", "pitwo.local", "pithree.local", "pifour.local",
        "pifive.local", "pisix.local", "piseven.local", "pieight.local"
    ] @=> string hostnames[];

    hostnames.size() => int NUM_PIS;
    float values[NUM_PIS];

    OscIn ultrasonicIn;
    OscMsg msg;

    OscOut ultrasonicOut[NUM_PIS];

    12345 => int DEFAULT_IN_PORT;
    5000 => int DEFAULT_OUT_PORT;

    fun void setInPort(int port) {
        port => ultrasonicIn.port;
    }

    fun void setOutPort(int port) {
        for (0 => int i; i < NUM_PIS; i++) {
            ultrasonicOut[i].dest(hostnames[i], DEFAULT_OUT_PORT);
        }
    }

    setInPort(DEFAULT_IN_PORT);
    setOutPort(DEFAULT_OUT_PORT);

    fun void listen() {
        spork ~ listener();
    }

    fun void listener() {
        while (true) {
            ultrasonicIn => now;
            while (ultrasonicIn.recv(msg)) {
                if (msg.address == "/w") {
                    for (0 => int i; i < hostnames.size(); i++) {
                        if ((msg.getString(0) + ".local") == hostnames[i]) {
                            msg.getFloat(1) => values[i];
                        }
                    }
                }
            }
            1::samp => now;
        }
    }
}
