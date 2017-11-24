from flask import request, Flask
from rsa import *
import json
import requests

key = genkeys()
private_key = key[0], key[2]
public_key = key[1], key[2]

conn = requests.post("http://127.0.0.1:9000/register", data = {'content': json.dumps(public_key)})
sig = json.loads(conn.text)

server = Flask(__name__)

@server.route('/signature', methods=['GET'])
def signature():
    return json.dumps(sig)

@server.route('/publickey', methods=['GET'])
def publickey():
    return json.dumps(public_key)

@server.route('/msg', methods=['POST'])
def msg():
    emsg = request.form['message']
    client_public_key = json.loads(request.form['client_public_key'])
    dmsg = decryptstr(int(emsg), private_key[0], private_key[1])
    print(dmsg)
    drpl = dmsg[::-1]
    erpl = str(encryptstr(drpl, client_public_key[0], client_public_key[1]))
    return erpl

server.run('127.0.0.1', 9002)