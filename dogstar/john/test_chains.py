import chains

chain = chains.make_quaternary_chain(8)
print(chain)

freqs = chains.convert_to_freqs(chain, (2, 1.5))
