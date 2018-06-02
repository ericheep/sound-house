// UltrasonicHandler
// written by Eric heep

// Dog Star 2018
// ~-~-

public class UltrasonicHandler {

    OscIn ultrasonicIn;
    OscMsg msg;

    OscOut ultrasonicOut[0];
    float values[0][0];
    string hostnames[0];
    0 => int NUM_PIS;
    10 => int filterSize;
    100::ms => dur pingCycle;

    int schmidtLatch[0];
    30.0 => float schmidtMax;
    10.0 => float schmidtMin;

    300.0 => float maxDistance;
    10.0 => float minDistance;
    0 => int emulation;

    class PassingEvent extends Event {
        int value;
        float reading;
    }
    PassingEvent passingEvent;

    fun void init(string _hostnames[], int outPort, int inPort) {
        _hostnames @=> hostnames;
        inPort => ultrasonicIn.port;
        ultrasonicIn.listenAll();
        hostnames.size() => NUM_PIS;
        values.size(NUM_PIS);
        schmidtLatch.size(NUM_PIS);

        for (0 => int i; i < NUM_PIS; i++) {
            OscOut oscOut;
            ultrasonicOut << oscOut;
            ultrasonicOut[i].dest(hostnames[i], outPort);

            float filterArray[filterSize];
            filterArray @=> values[i];
        }

        if (emulation) {
            randomEvents(NUM_PIS);
        } else {
            spork ~ ping();
            spork ~ listen();
        }
    }

    fun void setEmulation() {
        1 => emulation;
    }

    fun void setPing(dur p) {
        p => pingCycle;
    }

    fun void ping() {
        while (true) {
            for (0 => int i; i < NUM_PIS; i++) {
                ultrasonicOut[i].start("/w");
                ultrasonicOut[i].add(0);
                ultrasonicOut[i].send();
                pingCycle => now;
            }
        }
    }

    fun void listen() {
        while (true) {
            ultrasonicIn => now;
            while (ultrasonicIn.recv(msg)) {
                parseOsc(msg);
            }
        }
    }

    fun float mean(float arr[]) {
        arr.size() => int N;

        0.0 => float sum;
        for (0 => int i; i < N; i++) {
            arr[i] +=> sum;
        }
        return sum/N;
    }

    fun float std(float arr[]) {
        arr.size() => int N;
        mean(arr) => float _mean;

        0.0 => float sum;
        for (0 => int i; i < N; i++) {
            Math.pow(arr[i] - _mean, 2) +=> sum;
        }

        return Math.sqrt(sum/(N - 1.0));
    }

    fun void schmidtTrigger(float val, int index) {
        if (val > schmidtMax && schmidtLatch[index]) {
            0 => schmidtLatch[index];
            handleEvent(val, index);
        }
        if (val < schmidtMin) {
            1 => schmidtLatch[index];
        }
    }

    fun void randomEvents(int num) {
        for (0 => int i; i < num; i++) {
            spork ~ randomEvent(i);
        }
    }

    fun void randomEvent(int index){
        while (true) {
            index => passingEvent.value;
            passingEvent.signal();
            Math.random2f(0.5, 2.0) * second => now;
        }
    }

    fun void handleEvent(float val, int index) {
        index => passingEvent.value;
        val => passingEvent.reading;
        passingEvent.signal();
    }

    fun void parseOsc(OscMsg msg) {
        if (msg.address == "/w") {
            for (0 => int i; i < NUM_PIS; i++) {
                if ((msg.getString(0) + ".local") == hostnames[i]) {
                    msg.getFloat(1) => float reading;

                    // filters out strange readings
                    if (reading < 1000.0 && reading > 0.0) {
                        Std.clampf(reading, maxDistance, minDistance) => reading;
                        updateValues(reading, values[i]);
                        schmidtTrigger(std(values[i]), i);
                    }
                }
            }
        }
    }

    fun void updateValues(float value, float arr[]) {
        arr.size() => int N;
        for (N - 1 => int i; i > 0; i--) {
            arr[i - 1] => arr[i];
        }
        value => arr[0];
    }
}
