from flask import request, Flask
from rsa import *
import hashlib
import json
import requests

conn = requests.get("http://127.0.0.1:9002/")
ca = json.loads(conn.text)

conn = requests.get("http://127.0.0.1:9000/check")
ca_public_key = json.loads(conn.text)

md5 = hashlib.md5(ca['Content'].encode('utf-8')).hexdigest()

expectedmd5 = decryptstr(ca['Signature'], ca_public_key[0], ca_public_key[1])

if md5 == expectedmd5:
    print("check successfully")
    ca_content = json.loads(ca['Content'])

    message = input()

    emsg = str(encryptstr(message, ca_content[0], ca_content[1]))
    conn = requests.post("http://127.0.0.1:9002/msg", data={'message': emsg})
    erpl = conn.text
    drpl = decryptstr(int(erpl), ca_content[0], ca_content[1])
    print(drpl)
else:
    print("checking failed")