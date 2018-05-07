// PiHandler
// written by Eric heep

// Dog Star 2018
// ~-~-

public class PiHandler {

    [
        "pione.local", "pitwo.local", "pithree.local", "pifour.local",
        "pifive.local", "pisix.local", "piseven.local", "pieight.local"
    ] @=> string hostnames[];

    hostnames.size() => int NUM_PIS;

    OscOut piOut[8];
    OscMsg msg;

    fun void setOutPort(int port) {
        for (0 => int i; i < NUM_PIS; i++) {
            piOut[i].dest(hostnames[i], port);
        }
    }

}
