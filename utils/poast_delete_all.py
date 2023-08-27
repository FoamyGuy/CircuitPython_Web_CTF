import requests


resp = requests.post("http://192.168.1.119/dev/delete_all/", headers={"Authorization": "Bearer #CTF{ERV0Ja1_u0MNXHDfeMN339CR0hqQx1c8cRhdtby4pH5M}"})

print(resp.status_code)
print(resp.json())