// Stone2
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Stone2 extends Chubgraph {
    SndBuf w => LPF lpf => ADSR env;
    lpf.freq(2000);
    w.gain(0.5);

    int running;

    fun void connect() {
        env => outlet;
        1 => running;
    }

    fun void disconnect() {
        env =< outlet;
        0 => running;
    }

    fun void fallingRate(float initialRate) {
        float inc;
        while (initialRate - inc > 0 && running) {
            -0.00005 -=> inc;
            w.rate(initialRate - inc);
            5::ms => now;
        }
    }

    fun void trigger(float progress) {
        connect();

        (progress - 1.0) * 1.0 => float reverse;

        w.read("stone-2.wav");
        reverse  * 0.4 + 0.6 => float initialRate;
        w.rate(initialRate);

        1 => running;
        spork ~ fallingRate(initialRate);

        w.pos(0);
        env.attackTime(20::ms);
        env.sustainLevel(1.0);
        env.keyOn();
        20::ms => now;

        env.releaseTime(5::second);
        env.keyOff();
        5::second => now;

        disconnect();
    }

    fun int isRunning() {
        return running;
    }
}
