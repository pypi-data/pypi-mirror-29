import sys, copy, yaml, pprint
import simplejson as json
sys.path.append("../pukala")
from pukala import grow, ContextBase, PukalaBaseException
from fs_binding import FsBinding

CERT_FILE = "/home/pauls/.ssh/id_rsa.pub"
USERNAME = "pauls"
HOST = "localhost"
PORT = 7186

def fs_binding_exec_remote():
    class CC(object):
        def __init__(self):
            self.fs = FsBinding("fs.", self)
        def extract(self, context):
            return context.args[0]["err"][0].split()[0]
    data = {
        "some_call": ["_fcall", "extract",
                      ["_fcall", "fs.exec_remote",
                       CERT_FILE, USERNAME, HOST,
                       "python --version", {"port": PORT}]]
    }
    gr = grow(data, CC())
    correct = """
_history:
  fcalls_evaluated:
  - - single_call
    - extract
    - [some_call]
some_call: Python
"""
    assert(gr == yaml.load(correct))

def fs_binding_send_file():
    class CC(object):
        def __init__(self):
            self.fs = FsBinding("fs.", self)
    data = {
        "steps": [
            ["_fcall", "fs.exec_local", ["rm", "-f", "/tmp/foo2.txt"]],
            ["_fcall", "fs.send_file", "./dir0/foo2.txt", CERT_FILE, USERNAME, HOST, "/tmp", {"port": PORT}],
            ["_fcall", "fs.exec_local", ["ls", "/tmp/foo2.txt"]]
        ]
    }
    gr = grow(data, CC())
    
    correct = """
_history:
  fcalls_evaluated:
  - - single_call
    - fs.exec_local
    - [steps, 0]
  - - single_call
    - fs.send_file
    - [steps, 1]
  - - single_call
    - fs.exec_local
    - [steps, 2]
steps:
- cmd: [rm, -f, /tmp/foo2.txt]
  cwd: null
  err: ['']
  out: ['']
- cmd: null
  cwd: null
  err: ['']
  out: ['']
- cmd: [ls, /tmp/foo2.txt]
  cwd: null
  err: ['']
  out: [/tmp/foo2.txt, '']
"""
    gr["steps"][1]["cmd"] = None
    assert(gr == yaml.load(correct))

def fs_binding_get_file():
    class CC(object):
        def __init__(self):
            self.fs = FsBinding("fs.", self)
    data = {
        "steps": [
            ["_fcall", "fs.send_file", "./dir0/foo2.txt", CERT_FILE, USERNAME, HOST, "/tmp", {"port": PORT}],
            ["_fcall", "fs.exec_local", ["rm", "-rf", "/tmp/bubaa"]],
            ["_fcall", "fs.exec_local", ["mkdir", "/tmp/bubaa"]],
            ["_fcall", "fs.get_file", "/tmp/foo2.txt", CERT_FILE, USERNAME, HOST, "/tmp/bubaa", {"port": PORT}],
            ["_fcall", "fs.exec_local", ["ls", "/tmp/bubaa"]]
        ]
    }
    gr = grow(data, CC())
    correct = """
_history:
  fcalls_evaluated:
  - - single_call
    - fs.send_file
    - [steps, 0]
  - - single_call
    - fs.exec_local
    - [steps, 1]
  - - single_call
    - fs.exec_local
    - [steps, 2]
  - - single_call
    - fs.get_file
    - [steps, 3]
  - - single_call
    - fs.exec_local
    - [steps, 4]
steps:
- cmd: null
  cwd: null
  err: ['']
  out: ['']
- cmd: [rm, -rf, /tmp/bubaa]
  cwd: null
  err: ['']
  out: ['']
- cmd: [mkdir, /tmp/bubaa]
  cwd: null
  err: ['']
  out: ['']
- cmd: null
  cwd: null
  err: ['']
  out: ['']
- cmd: [ls, /tmp/bubaa]
  cwd: null
  err: ['']
  out: [foo2.txt, '']
"""
    for i in [0, 3]:
        gr["steps"][i]["cmd"] = None
    assert(gr == yaml.load(correct))


def fs_binding_exec_remote_batch():
    class CC(object):
        def __init__(self):
            self.fs = FsBinding("fs.", self)
        def extract(self, context):
            return context.args[0]["err"][0].split()[0]
    data = {
        "some_call": ["_fcall", "fs.exec_remote_batch",
                       CERT_FILE, USERNAME, HOST,
                       ["test -e /tmp && echo '11'",
                        "test -e /tmp && echo '22'",
                        "echo 'buba' 1>&2"
                    ], {"port": PORT}]
    }
    gr = grow(data, CC())
    correct = """
_history:
  fcalls_evaluated:
  - - single_call
    - fs.exec_remote_batch
    - [some_call]
some_call:
  cmd: null
  cwd: null
  err: [buba, '']
  out: ['11', '22', '']
"""
    gr["some_call"]["cmd"] = None
    assert(gr == yaml.load(correct))

def fs_binding_open_remote_folder_with_text_file():
    class CC(object):
        def __init__(self):
            self.fs = FsBinding("fs.", self)

        def get_fs_conf(self, context):
            z = self.fs.get_defaults(context)
            z["ftypes"][-1] = ['^folder://.*$', 'open_folder']
            return z

    data = {
        "fs_conf": ["_fcall", "get_fs_conf"],
        "steps": [
            ["_fcall", "fs.exec_local", ["rm", "-rf", "/tmp/dir0"]],
            ["_fcall", "fs.exec_local", ["cp", "-r", "./dir0", "/tmp"]],
            ["_fcall", "fs.open_inode", {
                "path": "/tmp/dir0",
                "host": HOST,
                "cert-file": CERT_FILE,
                "username": USERNAME,
                "opts": {
                    "port": PORT
                }
            }, "fs_conf"]
        ]
    }
    gr = grow(data, CC())
    correct = """
_history:
  fcalls_evaluated:
  - - single_call
    - get_fs_conf
    - [fs_conf]
  - - single_call
    - fs.exec_local
    - [steps, 0]
  - - single_call
    - fs.exec_local
    - [steps, 1]
  - - single_call
    - fs.open_inode
    - [steps, 2]
fs_conf:
  ftypes:
  - ['^file://.*~$', ignored]
  - ['^file://.*\.txt$', text]
  - ['^file://.*\.cfg$', text]
  - ['^file://.*\.yml$', yaml]
  - ['^file://.*\.yaml$', yaml]
  - ['^file://.*\.json$', json]
  - ['^file://.*\.xml$', xml]
  - ['^file://.*$', closed_file]
  - ['^folder://.*$', open_folder]
  handlers:
    closed_file: ['["_fcall", "fs.pull_closed_file"]', '["_fcall", "fs.push_closed_file"]']
    closed_folder: ['["_fcall", "fs.pull_closed_folder"]', '["_fcall", "fs.push_closed_folder"]']
    ignored: ['["_fcall", "fs.pull_ignored"]', '["_fcall", "fs.push_ignored"]']
    json: ['["_fcall", "fs.pull_json"]', '["_fcall", "fs.push_json"]']
    open_folder: ['["_fcall", "fs.pull_open_folder"]', '["_fcall", "fs.push_open_folder"]']
    text: ['["_fcall", "fs.pull_text"]', '["_fcall", "fs.push_text"]']
    xml: ['["_fcall", "fs.pull_xml"]', '["_fcall", "fs.push_xml"]']
    yaml: ['["_fcall", "fs.pull_yaml"]', '["_fcall", "fs.push_yaml"]']
steps:
- cmd: [rm, -rf, /tmp/dir0]
  cwd: null
  err: ['']
  out: ['']
- cmd: [cp, -r, ./dir0, /tmp]
  cwd: null
  err: ['']
  out: ['']
- inode:
    contents:
      dir1:
        contents:
          foo.txt:
            contents: [haha, haha2, '']
            ftype: text
        ftype: open_folder
      foo2.txt:
        contents: [bobo, hoho, '']
        ftype: text
    ftype: open_folder
  path: null
"""
    assert(type(gr["steps"][2]["path"]) == dict)
    gr["steps"][2]["path"] = None
    assert(gr == yaml.load(correct))

def fs_binding_save_remote_folder_with_text_file():
    class CC(object):
        def __init__(self):
            self.fs = FsBinding("fs.", self)

        def get_fs_conf(self, context):
            z = self.fs.get_defaults(context)
            z["ftypes"][-1] = ['^folder://.*$', 'open_folder']
            return z
            
    data = {
        "fs_conf": ["_fcall", "get_fs_conf"],
        "steps": [
            ["_fcall", "fs.exec_local",
             ["rm", "-rf", "/tmp/a_dir0"]],
            ["_fcall", "fs.open_inode",
             "./dir0",
             "/fs_conf"],
            ["_fcall", "fs.save_inode", "../1", {
                "path": "/tmp/a_dir0",
                "host": HOST,
                "cert-file": CERT_FILE,
                "username": USERNAME,
                "opts": {
                    "port": PORT
                }
            }, "fs_conf"],
            ["_fcall", "fs.open_inode",
             "/tmp/a_dir0",
             "/fs_conf"],
        ]
    }
    gr = grow(data, CC())
    correct = """
_history:
  fcalls_evaluated:
  - - single_call
    - get_fs_conf
    - [fs_conf]
  - - single_call
    - fs.exec_local
    - [steps, 0]
  - - single_call
    - fs.open_inode
    - [steps, 1]
  - - single_call
    - fs.save_inode
    - [steps, 2]
  - - single_call
    - fs.open_inode
    - [steps, 3]
fs_conf:
  ftypes:
  - ['^file://.*~$', ignored]
  - ['^file://.*\.txt$', text]
  - ['^file://.*\.cfg$', text]
  - ['^file://.*\.yml$', yaml]
  - ['^file://.*\.yaml$', yaml]
  - ['^file://.*\.json$', json]
  - ['^file://.*\.xml$', xml]
  - ['^file://.*$', closed_file]
  - ['^folder://.*$', open_folder]
  handlers:
    closed_file: ['["_fcall", "fs.pull_closed_file"]', '["_fcall", "fs.push_closed_file"]']
    closed_folder: ['["_fcall", "fs.pull_closed_folder"]', '["_fcall", "fs.push_closed_folder"]']
    ignored: ['["_fcall", "fs.pull_ignored"]', '["_fcall", "fs.push_ignored"]']
    json: ['["_fcall", "fs.pull_json"]', '["_fcall", "fs.push_json"]']
    open_folder: ['["_fcall", "fs.pull_open_folder"]', '["_fcall", "fs.push_open_folder"]']
    text: ['["_fcall", "fs.pull_text"]', '["_fcall", "fs.push_text"]']
    xml: ['["_fcall", "fs.pull_xml"]', '["_fcall", "fs.push_xml"]']
    yaml: ['["_fcall", "fs.pull_yaml"]', '["_fcall", "fs.push_yaml"]']
steps:
- cmd: [rm, -rf, /tmp/a_dir0]
  cwd: null
  err: ['']
  out: ['']
- inode:
    contents:
      dir1:
        contents:
          foo.txt:
            contents: [haha, haha2, '']
            ftype: text
        ftype: open_folder
      foo2.txt:
        contents: [bobo, hoho, '']
        ftype: text
    ftype: open_folder
  path: ./dir0
- null
- inode:
    contents:
      dir1:
        contents:
          foo.txt:
            contents: [haha, haha2, '', '']
            ftype: text
        ftype: open_folder
      foo2.txt:
        contents: [bobo, hoho, '', '']
        ftype: text
    ftype: open_folder
  path: /tmp/a_dir0
"""
    assert(gr == yaml.load(correct))
    

all_cases_func = [
    fs_binding_exec_remote,
    fs_binding_send_file,
    fs_binding_get_file,
    fs_binding_exec_remote_batch,
    fs_binding_open_remote_folder_with_text_file,
    fs_binding_save_remote_folder_with_text_file,

]

def do_tests():
    test_names = [i.__name__ for i in all_cases_func]
    all_cases = dict([(i.__name__, i) for i in all_cases_func])
    cases = sys.argv[1:]
    if not cases:
        cases = test_names
    for i in cases:
        print "#### %s ###" % i
        all_cases[i]()

if __name__ == "__main__":
    try:
        do_tests()
    except PukalaBaseException as e:
        print e.doc
        print e.get_formed_desc()
    # attempt to stop exceptions coming from python threading
    # infrastructure; ThreadPool.finish() just wakes them up,
    # not joining (which is correct, as threads may be stuck);
    # and apparently there is something which causes exception if
    # during shutdown thread tries to access lock or condition
    # variable
    import time
    time.sleep(0.1)
