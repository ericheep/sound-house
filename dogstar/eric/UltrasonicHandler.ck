// UltrasonicHandler
// written by Eric heep

// Dog Star 2018
// ~-~-

public class UltrasonicHandler {

    OscIn ultrasonicIn;
    OscMsg msg;

    OscOut ultrasonicOut[0];
    float values[0];
    string hostnames[0];
    0 => int NUM_PIS;

    fun void init(string _hostnames[], int outPort, int inPort) {
        _hostnames @=> hostnames;
        inPort => ultrasonicIn.port;
        ultrasonicIn.listenAll();
        for (0 => int i; i < hostnames.size(); i++) {
            OscOut oscOut;
            ultrasonicOut << oscOut;
            ultrasonicOut[i].dest(hostnames[i], outPort);
        }
        hostnames.size() => NUM_PIS;
        values.size(NUM_PIS);
    }

    fun void listen() {
        spork ~ listener();
    }

    fun void ping(dur cycleDuration) {
        spork ~ pinger(cycleDuration);
    }

    fun void pinger(dur cycleDuration) {
        while (true) {
            for (0 => int i; i < NUM_PIS; i++) {
                ultrasonicOut[i].start("/w");
                ultrasonicOut[i].add(0);
                ultrasonicOut[i].send();
                cycleDuration => now;
            }
        }
    }

    fun void parseOsc(OscMsg msg) {
        if (msg.address == "/w") {
            for (0 => int i; i < NUM_PIS; i++) {
                if ((msg.getString(0) + ".local") == hostnames[i]) {
                    msg.getFloat(1) => values[i];
                    <<< values[i] >>>;
                }
            }
        }
    }

    fun void listener() {
        while (true) {
            ultrasonicIn => now;
            while (ultrasonicIn.recv(msg)) {
                parseOsc(msg);
            }
        }
    }
}
