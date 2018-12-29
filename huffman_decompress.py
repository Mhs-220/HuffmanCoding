import os
import sys
import uuid
import huffmancoding

def decompressor(input_file, output_path):
	files_name, end = None, None
	with open(input_file, "r", encoding="latin1") as ninp:
		files_name, end = get_file_names(ninp)

	with open(input_file, "rb") as inp:
		inp.seek(end)
		bitin = huffmancoding.BitInputStream(inp)
		canoncode = read_code_len_table(bitin)
		code = canoncode.to_code_tree()
		decompress(code, bitin, output_path, files_name)

def read_code_len_table(bitin):
	def read_int(n):
		result = 0
		for _ in range(n):
			result = (result << 1) | bitin.read_no_eof()
		return result

	codelengths = [read_int(8) for _ in range(257)]
	return huffmancoding.CanonicalCode(codelengths=codelengths)


def get_file_names(ninp):
	content = ninp.read().replace('\n', '')
	start = content.find("[") + 1
	end = content.find("]")
	files_name = content[start:end].split("|")
	return files_name, end + 1


def decompress(code, bitin, out, files_name):
	dec = huffmancoding.HuffmanDecoder(bitin)
	dec.codetree = code
	filesname = [os.path.join(out, i) for i in files_name]
	output = [open(filename, 'wb') for filename in filesname]
	i = 0
	while True:
		symbol = dec.read()
		if symbol == 256:  # EOF symbol
			i += 1
			if i == len(output):
				break
		else:
			output[i].write(bytes((symbol,)))


# if __name__ == '__main__':
# 	decompressor("test3.mhs", "/home/mhs/PersonnalProjects/HuffmanCoding/")
