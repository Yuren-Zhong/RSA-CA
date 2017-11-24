from flask import request, Flask
from rsa import *
import hashlib
import json
import requests

key = genkeys()
private_key = key[0], key[2]
public_key = key[1], key[2]

conn = requests.get("http://127.0.0.1:9002/signature")
sig = json.loads(conn.text)
conn = requests.get("http://127.0.0.1:9002/publickey")
server_public_key = conn.text

conn = requests.get("http://127.0.0.1:9000/check")
ca_public_key = json.loads(conn.text)

md5 = hashlib.md5(server_public_key.encode('utf-8')).hexdigest()

expectedmd5 = decryptstr(sig, ca_public_key[0], ca_public_key[1])

if md5 == expectedmd5:
    print("check successfully")
    server_public_key = json.loads(server_public_key)

    message = input()

    emsg = str(encryptstr(message, server_public_key[0], server_public_key[1]))
    conn = requests.post("http://127.0.0.1:9002/msg", data={'message': emsg, 'client_public_key': json.dumps(public_key)})
    erpl = conn.text
    drpl = decryptstr(int(erpl), private_key[0], private_key[1])
    print(drpl)
else:
    print("checking failed")