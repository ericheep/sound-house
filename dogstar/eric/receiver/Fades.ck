// Fades
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Fades {
    CNoise p => TriOsc t => Dyno d => LPF lpf => WinFuncEnv win => PowerADSR env => dac;
    SinOsc s => blackhole;

    fun void test() {
        p.gain(1500);
        t.sync(2);
        lpf.freq(4000);
        t.freq(9000);

        spork ~ windowModulate();

        envelopePath(
            [1.0, 2.0, 3.0, 2.0, 4.0, 4.0]
        );
    }

    // TODO: change window modulate durations to drift independently

    fun void windowModulate() {
        while (true) {
            win.setParzen();
            win.keyOn();
            win.attackTime(5::ms);
            20::ms => now;
            win.keyOff();
            win.releaseTime(5::ms);
            20::ms => now;
        }
    }

    fun void envelopePath(float seconds[]) {
        seconds.size() => int N;
        for (0 => int i; i < N; i++) {
            seconds[i]::second => dur duration;
            if (i % 2 == 0) {
                env.attackCurve(Math.random2f(1.5, 2.5));
                env.attack(duration);
                env.keyOn();
            } else {
                env.releaseCurve(Math.random2f(0.25, 0.75));
                env.release(duration + Math.random2f(0.1, 0.25) * duration);
                env.keyOff();
            }
            duration => now;
        }

        seconds[seconds.size() - 1]::second => now;
    }
}

Fades f;
f.test();
