import sys
import numpy as np
import getopt
from funcs import *
from hashlib import md5


input_file = ""
passwd = 0
output_file = ""

usage = 'Usage:\n' + r'      python encrypt_decrypt_metadata.py -i input_file [Options]'
options = 'Options:\n'
options = options + r'      -h, --help                             Show help information' + '\n'
options = options + r'      -i, --input   <input file>             The NFT meta data file' + '\n'
options = options + r'      -p, --pass  password                    Password' + '\n'
options = options + r'      -o, --output  <output file>             Output file' + '\n'

opts,args = getopt.getopt(sys.argv[1:],'-h-i:-p:-o:',
                          ['help','input=','pass=',  'output='])

for opt_name,opt_value in opts:
    if opt_name in ('-h','--help'):
        print(usage)
        print(options)
        sys.exit()
    if opt_name in ('-i','--input'):
        input_file = opt_value
    if opt_name in ('-p','--pass'):
        passwd = opt_value
    if opt_name in ('-o','--output'):
        output_file = opt_value

if not input_file:
    print(usage)
    print(options)
    sys.exit()

file = open(input_file, 'rb')
filebytes = file.read()
file.close()
pass_bytes = int(passwd).to_bytes(4, 'big')
encrypted_meta_data = xor_l_s(filebytes, pass_bytes)



OUT = open(output_file, 'wb')
OUT.write(encrypted_meta_data)
OUT.close()

print("Your meta data file has been succefully encrypted!")
print("The encrypted file is: " + output_file)
print("MD5 value of your password [" + str(passwd) + "]:")
print(md5(pass_bytes).hexdigest())



