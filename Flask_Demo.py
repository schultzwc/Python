from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'I love Georgeann Marie Kolbow, and I cannot wait to move in with her <3'