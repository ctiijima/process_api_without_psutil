from flask import Flask, jsonify, request

import sys
import os

app = Flask(__name__)

def read_proc_cmdline(proc_file):
#Reads the CMDLINE and returns unless error hit
    try:
        with open(proc_file, 'r') as proc_fil:
            data = proc_fil.read()
            ret_val = (data.replace('\0', ' '))
    except PermissionError as pe:
        ret_val = ("Permission Error: {}".format(str(pe)))
    except Exception as e:
        ret_val = ("Exception: {}".format(str(xe)))
    except IOError as ioe:
        ret_val = ("IOError: {} ".format(str(ioe)))
    finally:
        return ret_val

def read_proc_environ(proc_file):
#Tries to read environ file
#This requires elevated permissions or will error a lot
    try:
        with open(proc_file, 'r') as proc_fil:
            data = proc_fil.read()
            ret_val = (data.replace('\0', ' '))
    except PermissionError as pe:
        ret_val = ("Permission Error: {} ".format(str(pe)))
    except Exception as e:
        ret_val = ("Exception: {}".format(str(xe)))
    except IOError as ioe:
        ret_val = ("IOError: {}".format(str(ioe)))
    finally:
        return ret_val

def read_proc_name(proc_file):
#Reads the status file and strips out the process name
    try:
        with open(proc_file, 'r') as proc_fil:
            data = proc_fil.readline()
            ret_val = (data[6:].replace('\0', ' ').rstrip())
    except PermissionError as pe:
        ret_val = ("Permission Error: {}".format(str(pe)))
    except Exception as e:
        ret_val = ("Exception: {}".format(str(xe)))
    except IOError as ioe:
        ret_val = ("IOError: {} ".format(str(ioe)))
    finally:
        return ret_val
                    
def list_dir():
#Lists all folders/pids in the /proc folder
#Strips out all the folder names that are not numeric
    path = '/proc'
    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name)) and name.isdigit()]
    return folders

@app.route('/ps', methods=['GET'])
#Main Flask app
def Processes():
    pids = list_dir()
    result_dict = {}
    for pid in pids:
        proc_cmdline = "/proc/{}/cmdline".format(pid)
        proc_environ = "/proc/{}/environ".format(pid)
        proc_name = "/proc/{}/status".format(pid)
        cmdline = read_proc_cmdline(proc_cmdline)
        environ = read_proc_environ(proc_environ)
        name = read_proc_name(proc_name)
        result_dict[pid] = {'NAME':name,'CMDLINE':cmdline, 'ENVIRON':environ}
    return jsonify(result_dict)

@app.route('/shutdown', methods=['POST'])
#Shuts down on post 
#not super secure, quick and dirty solution
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not a Werkzeug Server')
    func()
    return "Shutting down the Flask app..."

if __name__ == "__main__":
    app.run()

