from flask import request, Flask
from rsa import *
import json
import requests

key = genkeys()
private_key = key[0], key[2]
public_key = key[1], key[2]

conn = requests.post("http://127.0.0.1:9000/register", data = {'content': json.dumps(public_key)})
ca = json.loads(conn.text)

server = Flask(__name__)

@server.route('/', methods=['GET'])
def index():
    return json.dumps(ca)

@server.route('/msg', methods=['POST'])
def msg():
    emsg = request.form['message']
    dmsg = decryptstr(int(emsg), private_key[0], private_key[1])
    print(dmsg)
    drpl = dmsg[::-1]
    erpl = str(encryptstr(drpl, private_key[0], private_key[1]))
    return erpl

server.run('127.0.0.1', 9002)