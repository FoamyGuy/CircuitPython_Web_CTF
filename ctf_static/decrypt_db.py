from EasyCrypt import decrypt_string
import json

f = open("ctf_static/db_key.txt", "rb")
key = f.read()
f.close()
print(f"key: {key}")


f = open("ctf_static/encrypted_lazy_hosts_db.txt", "rb")
encrypted = f.read()
f.close()

print(encrypted)

print("-----")

decrypted = decrypt_string(key, encrypted, "")
print(json.loads(decrypted))


