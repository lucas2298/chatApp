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
    tags = running.responses(messRecive, userId)
    data = ""
    for tag in tags:
        data = data +"+"+tag
    return data

if __name__ == "__main__":
    app.run(port=4001)