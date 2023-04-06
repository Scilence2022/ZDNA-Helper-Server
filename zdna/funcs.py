from math import ceil


def charN(str, N):
    if N < len(str):
        return str[N]
    return 'X'


def oxor(str1, str2):
    length = max(len(str1), len(str2))
    return ''.join(chr(ord(charN(str1, i)) ^ ord(charN(str2, i))) for i in range(length))


def xor(str1, str2):
    length = max(len(str1), len(str2))
    if len(str1) > len(str2):
        str2 = str2 + bytes(len(str1) - len(str2))
    if len(str2) > len(str1):
        str1 = str1 + bytes(len(str2) - len(str1))
    allBytes = b''
    i = 0
    while i < length:
        allBytes = allBytes + bytes([str1[i] ^ str2[i]])
        i = i + 1
    return allBytes

def xor_l_s(str1, str2):
    chunk_size = len(str2)
    chunk_num = int(ceil(len(str1) / float(len(str2))))  #int(len(str1)/chunk_size)
    i = 0
    xor_data = b''
    while i < chunk_num:
        chunk_bytes = chunk_data(str1, chunk_size, i)
        chunk_pass = str2
        if len(chunk_bytes) < chunk_size:
            chunk_pass = str2[:len(chunk_bytes)]
        xor_data = xor_data + xor(chunk_bytes, chunk_pass)
        i = i + 1
    return xor_data


def chunk_data(data, chunk_size, num):
    #chunk_num = int(ceil(len(data) / float(chunk_size)))
    start = chunk_size * num
    end = min(chunk_size * (num + 1), len(data))
    return data[start:end]


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)