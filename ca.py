from flask import request, Flask
from rsa import *
import json
import requests
import hashlib

key = genkeys()
private_key = key[0], key[2]
public_key = key[1], key[2]

ca = Flask(__name__)

@ca.route('/register', methods = ['POST'])
def register():
    content = request.form['content']

    md5 = hashlib.md5(content.encode('utf-8')).hexdigest()

    reply = encryptstr(md5, private_key[0], private_key[1])
    return json.dumps(reply)

@ca.route('/check', methods = ['GET'])
def check():
    return json.dumps(public_key)

ca.run('127.0.0.1', 9000)