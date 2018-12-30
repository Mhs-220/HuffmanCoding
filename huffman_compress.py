import os
import sys
import contextlib
import huffmancoding

def compressor(input_files, output_file):
	# Read input file once to compute symbol frequencies.
	# The resulting generated code is optimal for static Huffman coding and also canonical.
	freqs = huffmancoding.FrequencyTable([0] * 257)
	files_count = len(input_files)
	for files in input_files:
		get_frequencies(files, freqs)
		freqs.increment(256)  # EOF symbol
	code = freqs.build_code_tree()
	canoncode = huffmancoding.CanonicalCode(tree=code, symbollimit=freqs.get_symbol_limit())
	# Replace code tree with canonical one. For each symbol,
	# the code value may change but the code length stays the same.
	code = canoncode.to_code_tree()

	# Read input file again, compress with Huffman coding, and write output file
	with contextlib.closing(huffmancoding.BitOutputStream(open(output_file + ".mhs", "wb"))) as bitout:
		inp = [open(filename, 'rb') for filename in input_files]
		files_name = [os.path.basename(f.name) for f in inp]
		write_code_len_table(bitout, canoncode, files_name)
		compress(code, inp, bitout, files_count)
		for file in inp:
			file.close()


# Returns a frequency table based on the bytes in the given file.
# Also contains an extra entry for symbol 256, whose frequency is set to 0.
def get_frequencies(filepath, freqs):
	with open(filepath, "rb") as input:
		while True:
			b = input.read(1)
			if len(b) == 0:
				break
			b = b[0]
			freqs.increment(b)
	return freqs


def write_code_len_table(bitout, canoncode, files_name):
	bitout.output.write(bytes("[", 'utf-8'))
	for i in range(0, len(files_name)):
		bitout.output.write(bytes(files_name[i], 'utf-8'))
		if i != (len(files_name) - 1):
			bitout.output.write(bytes("|", 'utf-8'))
	bitout.output.write(bytes("]", 'utf-8'))
	for i in range(canoncode.get_symbol_limit()):
		val = canoncode.get_code_length(i)
		# For this file format, we only support codes up to 255 bits long
		if val >= 256:
			raise ValueError("The code for a symbol is too long")

		# Write value as 8 bits in big endian
		for j in reversed(range(8)):
			bitout.write((val >> j) & 1)


def compress(code, inp, bitout, files_count):
	enc = huffmancoding.HuffmanEncoder(bitout)
	enc.codetree = code
	for i in range(0, files_count):
		while True:
			b = inp[i].read(1)
			if len(b) == 0:
				break
			enc.write(b[0])
		enc.write(256)  # EOF
