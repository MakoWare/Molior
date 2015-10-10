from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, send_file

app = Flask(__name__)

@app.route("/")
def test():
    print ('got a request')
    if request.headers.get('X-GitHub-Event') == "ping":
        return json.dumps({'msg': 'Hi!'})
    if request.headers.get('X-GitHub-Event') != "push":
        return json.dumps({'msg': "wrong event type"})


if __name__ == '__main__':
    app.debug = True
    app.run()
