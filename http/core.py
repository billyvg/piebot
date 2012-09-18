from flask import Flask, request
app = Flask(__name__)

@app.route("/github", methods=['POST'])
def github():
    print request
