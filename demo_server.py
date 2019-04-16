from flask import Flask, session, Response, request
from session_manager import MolSession
import json
import base64

app = Flask(__name__)


@app.route('/molcaptcha')
def run():
    answer = ''

    if 'mol' not in session:
        session['mol'] = MolSession()
    else:
        answer = request.args.get('answer')

    mol = MolSession(session['mol'])
    result = False
    if answer:
        result = mol.response_captcha(answer)
    resp = Response(json.dumps({
        "captcha": "data:image/png;base64," + str(base64.b64encode(mol.get_captcha()), encoding='ascii'),
        "result": result
    }))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = 'http://molcaptcha.imtwice.cn'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'

    return resp


if __name__ == '__main__':
    app.secret_key = b'\x93TD\x9b\n\xedt[+\xd0\xe0K\xb4>s\xe2'
    app.run()
