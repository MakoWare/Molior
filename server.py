from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, send_file
import json
import subprocess
import os

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

    ##First Change the Directory
    f = open('config.txt', 'r')
    config = json.loads(f.read())
    dir = config['dir']
    commands = config['commands']
    print(dir)
    retval = os.getcwd()
    print ("Current working directory %s" % retval)
    os.chdir(os.path.expanduser(dir))
    retval = os.getcwd()
    print ("Directory changed successfully %s" % retval)

    print(commands)
    for command in commands:
         print(command)
         subprocess_cmd(command)

    #p = subprocess.Popen([command, argument1,...], cwd=working_directory)
    #p.wait()

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)

if __name__ == '__main__':
    run()
    # app.debug = True
    # app.run(host='0.0.0.0', port=80)
    # app.run()
