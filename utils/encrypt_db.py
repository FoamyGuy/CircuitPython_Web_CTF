# import aesio
# from binascii import hexlify
#
# key = b'Sixteen byte key'
# inp = b'CircuitPython!!! Mmmm bytes Keep adding stuff more stuff ?ds slkdweoruweoriuweoiruweoiruewoiruewoiru' # Note: 16-bytes long
# outp = bytearray(len(inp))
# cipher = aesio.AES(key, aesio.MODE_CTR)
# cipher.encrypt_into(inp, outp)
# print(outp)
#
# decrypt_buf = bytearray(len(outp))
#
# cipher.decrypt_into(outp, decrypt_buf)
#
# print(bytes(decrypt_buf))
#
#



# from EasyCrypt import encrypt_string, decrypt_string
# ivstring = "aba0a3bde34a03487eda3ec96d5736a8"
# key = b'#CTF{CryptoFail}'
# # #CTF{CryptoFail}
# inp = b'CircuitPython!!! Mmmm bytes Keep adding stuff more stuff ?ds slkdweoruweoriuweoiruweoiruewoiruewoiru' # Note: 16-bytes long
#
# encrypted = encrypt_string(key, inp, "")
# print(encrypted)
# print('----')
# decrypted = decrypt_string(key, encrypted, "")
# print(decrypted)
#
#
#


import binascii
from EasyCrypt import encrypt_string

f = open("ctf_static/lazy_hosts_db.json", "rb")
db_data = f.read()
f.close()

f = open("../ctf_static/db_key.txt", "rb")
key = f.read()
f.close()

encrypted = encrypt_string(key, db_data, "")
print(encrypted)

#print('Encrypted:', binascii.hexlify(encrypted))

# f = open("encrypted_lazy_hosts_db.txt", 'wb')
# f.write(binascii.hexlify(ciphertext))
# f.close()
