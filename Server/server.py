# Server chạy Flask

from flask import Flask, request
import json
import running
import base64

app = Flask(__name__)
@app.route('/')
def index():
    return "Flask server"

@app.route('/postdata', methods = ['POST'])
def postdata():
    data = request.get_json()
    messRecive = ""
    userId = ""
    temp = ""
    for i in data:
        if i != '+':
            temp += i
        else:
            messRecive = temp
            temp = ""
    userId = temp

    messRes = running.responses(messRecive, userId)
    messSum = ""
    for mess in messRes:
        messSum = messSum + '\n' + mess
    messSum += '\n'

    encodedBytes = base64.b64encode(messSum.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    return encodedStr

if __name__ == "__main__":
    app.run(port=4001)