from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, send_file
import json
import subprocess
import os

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def test():
    print ('got a request')
    if request.headers.get('X-GitHub-Event') == "ping":
        runTasks(request)
        return json.dumps({'msg' : "We Livin"})
    elif request.headers.get('X-GitHub-Event') != "push":
        return json.dumps({'msg': "wrong event type"})
    else:
        runTasks(request)
        return json.dumps({'msg': "building"})


def runTasks(request):
    data = json.loads(request.data.decode("utf-8"))
    repoName = data['repository']['name']
    repoPath = '~/Repos/' + repoName
    repoBranch = data['ref'].split("/")[-1]

    print("running tasks")
    print(json.dumps(data, indent=2, sort_keys=True))
    print("repoName: %s" % repoName)
    print("repoPath: %s" % repoPath)
    print("repoBranch: %s" % repoBranch)

    ##Save CWD
    cwd = os.getcwd()

    ##Change to Repo Dir
    os.chdir(os.path.expanduser(repoPath))

    ##Load the Config
    f = open('molior.json', 'r')
    config = json.loads(f.read())
    branches = config['branches']
    branchCommands = branches[repoBranch]['commands']
    print(json.dumps(config, indent=2, sort_keys=True))
    print(branchCommands)

    for command in branchCommands:
        print(command)
        subprocess_cmd(command)

    os.chdir(os.path.expanduser(cwd))

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    app.run()
