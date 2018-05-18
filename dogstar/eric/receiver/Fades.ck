// Fades
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Fades {
    CNoise p => TriOsc t => Dyno d => LPF lpf => PowerADSR env => dac;
    SinOsc s => blackhole;

    fun void test() {
        p.gain(800);
        t.sync(2);
        lpf.freq(1200);
        t.freq(500);

        envelopePath(
            [2.0, 0.5, 2.0, 0.5, 2.0, 0.5],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        );
    }

    fun void envelopePath(float curves[], float seconds[]) {
        curves.size() => int N;
        for (0 => int i; i < N; i++) {
            seconds[i]::second => dur duration;
            if (i % 2 == 0) {
                env.attackCurve(curves[i]);
                env.attack(duration);
                env.keyOn();
            } else {
                env.releaseCurve(curves[i]);
                env.release(duration + Math.random2f(0.33, 1.0) * duration);
                env.keyOff();
            }
            duration => now;
        }

        seconds[seconds.size() - 1]::second => now;
    }
}

Fades f;
f.test();
