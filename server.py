from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, send_file
import json
import subprocess
app = Flask(__name__)

repositoryName = ""

@app.route("/", methods=['GET', 'POST'])
def test():
    print ('got a request')
    if request.headers.get('X-GitHub-Event') == "ping":
        parseResponse(request)
        print(repositoryName)
        return json.dumps(repositoryName)
    if request.headers.get('X-GitHub-Event') != "push":
        print (request.data.decode("utf-8"))
        return json.dumps({'msg': "wrong event type"})


def parseResponse(response):
    global repositoryName
    data = json.loads(request.data.decode("utf-8"))
    repositoryName = data['repository']['name']
    return

def run():
    p = subprocess.Popen([command, argument1,...], cwd=working_directory)
    p.wait()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
    app.run()
