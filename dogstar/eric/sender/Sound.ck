// Sound

// written by Eric Heep
// Dog Star 2018
// ~-~-

public class Sound {
   dur start;
   dur end;
   string address;
   float progress;

   fun void set(string addr, dur s, dur e) {
        addr => address;
        s => start;
        e => end;
   }

   fun float getProgress(time currentTime) {
        if (currentTime/samp > start/samp && currentTime/samp < end/samp) {
            currentTime/samp - start/samp => float position;
            end/samp - start/samp => float total;
            return position/total;
        } else {
            return -1.0;
        }
   }

   fun string getAddress() {
        return address;
   }
}
