// Bumps
// written by Eric heep

// Dog Star 2018
// ~-~-

public class Bumps extends Chubgraph {

    class Distortion extends Chugen {
        fun float tick(float in) {
            Math.pow(in, 0.75) => in;

            while (in > 1.0 || in < -1.0) {
                if (in > 1.0) {
                    1.0 - (in - 1.0) => in;
                }
                if (in < -1.0) {
                    -1.0 - (in + 1.0) => in;
                }
            }
            return in;
        }
    }

    Noise noise => LPF lpf => Dyno d => ADSR env => Distortion dist;

    int running;

    fun void connect() {
        1 => running;
        dist => outlet;
    }

    fun void disconnect() {
        0 => running;
        dist =< outlet;
    }

    fun void trigger(float progress) {
        connect();
        (progress - 1.0) * -1.0 => float reverse;
        noise.gain(1.0 - reverse * 0.7);

        lpf.freq(200 + 400 * reverse);
        Math.pow(reverse, 6) => float revExp;

        0.75::second => dur range;
        100::ms => dur min;
        10::ms + 10::ms * revExp => dur attackTime;

        revExp * range + min => dur bumpDur;

        repeat(2) {
            env.attackTime(attackTime);
            env.sustainLevel(1.0);
            env.keyOn();
            attackTime => now;
            env.releaseTime(attackTime);
            env.keyOff();
            bumpDur => now;
        }
        disconnect();
    }

    fun int isRunning() {
        return running;
    }
}

Bumps b => dac;
b.trigger(0.0);
