for (int i; i < 8; i++) {
	adc.chan(i) => Gain g => dac;
}

while (true) {
<<<	Std.rmstodb(adc.chan(0).last()) >>>;
	100::ms => now;
}
