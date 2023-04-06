import sys
import numpy as np
import getopt
from funcs import *
from hashlib import md5


input_file = ""
passwd = 0
old_passwd = 0
output_file = ""

usage = 'Usage:\n' + r'      python encrypt_decrypt_metadata.py -i input_file [Options]'
options = 'Options:\n'
options = options + r'      -h, --help                             Show help information' + '\n'
options = options + r'      -n, --newpass  password                   The new password' + '\n'
options = options + r'      -o, --oldpass  password                The old password' + '\n'



opts,args = getopt.getopt(sys.argv[1:],'-h-n:-o:',
                          ['help','input=','pass=',  'output='])

for opt_name,opt_value in opts:
    if opt_name in ('-h','--help'):
        print(usage)
        print(options)
        sys.exit()

    if opt_name in ('-n','--newpass'):
        passwd = opt_value
    if opt_name in ('-o','--oldpass'):
        old_passwd = opt_value





pass_bytes = int(passwd).to_bytes(4, 'big')
old_pass_bytes = int(old_passwd).to_bytes(4, 'big')

xor_pass_bytes = xor(old_pass_bytes, pass_bytes)
xor_pass = int.from_bytes(xor_pass_bytes, 'big')


print("Please use the following number for password updating:")
print(xor_pass)
print("MD5 hash of your old password:", end="\t")
print(md5(old_pass_bytes).hexdigest())

print("MD5 hash of your new password:", end="\t")
print(md5(pass_bytes).hexdigest())


