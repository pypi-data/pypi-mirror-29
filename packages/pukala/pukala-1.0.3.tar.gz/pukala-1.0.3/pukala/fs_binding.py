import re, os, os.path, yaml, shutil, subprocess, copy, pipes
import simplejson as json

import xml.etree.ElementTree as ET
from pukala import FCall, Path, PukalaBaseException, CallContext

# consists of few parts:
# - local / remote execution possibility
# - fs reflection back and forth possibility
#   - file system is reflected by copying folder structure inside
#     doctree
#   - files are open and their contents added to the doctree
#   - both files and folders can be kept closed, thus avoiding
#     unnecessary information in the tree
#   - binary files (distinguished by their name) are kept closed by
#     default
#   - it is possible to write custom handlers for both push and pull
#     operations
#   - closed files are simply copied from their locations when
#     reflecting back
#   - executed handlers doesn't reflect in history, they bypass
#     common execution mechanics

class PukalaFsException(PukalaBaseException):
    def __init__(self, cmd, cwd, retcode, out, err, cause=None):
        PukalaBaseException.__init__(self, "command execution failed", cause)
        self.cmd = cmd
        self.cwd = cwd
        self.retcode = retcode
        self.out = out
        self.err = err

    def get_desc(self):
        d = PukalaBaseException.get_desc(self)
        return [
            "err: %s\n" % str(self.err),
            "out: %s\n" % str(self.out),
            "retcode: %d\n" % self.retcode,
            "cwd: %s\n" % str(self.cwd),
            "cmd: %s\n" % str(self.cmd),
        ] + d

# we use CallContext extensions to pass more sophisticated methods
# to handlers than CallContext provides; main intent is to have
# it as "transport layer"; handlers (their fcalls) are file-type
# specific, whereas handler contexts are main fcall (open_inode,
# save_inode) specifc

class AbstractHandlerContext(CallContext):
    def __init__(self, context, fs_binding):
        CallContext.__init__(self, context.doc, context.path,
                             context.args)
        self.fpath = context.args[0]
        self.fs_binding = fs_binding
    def set_path(self, path):
        self.fpath = path
        self.args[0] = path
    def get_inode_path_desc(self):
        pass

    def clone(self, args=None, deep=False):
        return CallContext.clone(self, args, deep=False)

    def _exec_remote(self, fpath, cmd):
        ctx2 = self.clone([
            fpath["cert-file"],
            fpath["username"],
            fpath["host"],
            cmd,
            fpath.get("opts", {}),
        ])
        return self.fs_binding.exec_remote(ctx2)

    def clean_up(self):
        pass

class AbstractPullContext(AbstractHandlerContext):
    def read(self):
        pass

    def read_folder(self):
        pass

    def do_pull(self, path):
        pass

    def check_path_exists(self):
        pass
        
    @staticmethod
    def create_pull_handler(context, fs_binding):
        is_local = type(context.args[0]) == str
        if is_local:
            return LocalPullContext(context, fs_binding)
        else: 
            return RemotePullContext(context, fs_binding)


class AbstractPushContext(AbstractHandlerContext):
    def __init__(self, context, fs_binding, inode_path, source):
        AbstractHandlerContext.__init__(self, context, fs_binding)
        self.inode_path = inode_path
        self.source = source
        self.fpath = context.args[1]

    def clone(self, args=None, deep=False):
        res = AbstractHandlerContext.clone(self, args)
        res.fpath = copy.deepcopy(self.fpath)
        # ugly as hell...
        if not args:
            res.args[1] = res.fpath
        return res

    def set_path(self, path):
        self.fpath = path
        self.args[1] = path

    def write(self, data):
        pass

    def create_folder(self):
        pass

    def write_from_path(self, path):
        pass

    def write_folder_from_path(self, path):
        pass

    def do_push(self, path_suffix, source):
        pass

    def _write_local(self, data):
        with open(self.fpath, "w") as f:
            f.write(data)

    def _create_folder_local(self):
        if os.path.exists(self.fpath):
            raise Exception("path exists %s" % self.fpath)
        os.makedirs(self.fpath)

    def _write_from_path_local(self):
        if self.inode_path != self.fpath:
            shutil.copyfile(self.inode_path, self.fpath)

    def _write_folder_from_path_local(self):
        if self.inode_path == self.fpath:
            return
        if os.path.exists(self.fpath):
            raise Exception("path exists %s" % self.fpath)
        shutil.copytree(self.inode_path, self.fpath)

    def _do_push_local(self, path_suffix, source):
        self.set_path(os.path.join(self.fpath, path_suffix))

        if type(self.inode_path) == str:
            self.inode_path = "%s/%s" % (self.inode_path,
                                         path_suffix)
        else:
            self.inode_path["path"] = "%s/%s" % (
                self.inode_path["path"], path_suffix)
        self.source = source
        self.args[0] = source
        return self.fs_binding.save_inode(self)

    def _write_remote(self, data):
        cmd = "echo %s >> %s" % (pipes.quote(data),
                                 self.fpath["path"])
        self._exec_remote(self.fpath, cmd)

    def _create_folder_remote(self):
        p = self.fpath["path"]
        cmd = "test -e %s && echo 'folder exists' && exit 1 || mkdir -p %s" % (p, p)
        self._exec_remote(self.fpath, cmd)

    def _write_from_path_remote(self):
        with open(self.inode_path, "r") as f:
            data = f.read()
        self.write(data)

    def _write_folder_from_path_remote(self):
        p = self.fpath["path"]
        cmd = "test -e %s && echo 'folder exists' && exit 1" % p
        self._exec_remote(self.fpath, cmd)
        ctx2 = self.clone([
            self.inode_path,
            fpath["cert-file"],
            fpath["username"],
            fpath["host"],
            p,
            fpath.get("opts", {}),
        ])
        return self.fs_binding.send_file(ctx2)

    def _do_push_remote(self, path_suffix, source):
        self.fpath["path"] = "%s/%s" % (self.fpath["path"],
                                        path_suffix)
        self.args[1] = self.fpath

        if type(self.inode_path) == str:
            self.inode_path = "%s/%s" % (self.inode_path,
                                         path_suffix)
        else:
            self.inode_path["path"] = "%s/%s" % (
                self.inode_path["path"], path_suffix)
        self.source = source
        self.args[0] = source
        return self.fs_binding.save_inode(self)
        

    @staticmethod
    def create_push_handler(context, fs_binding, inode_path,
                            source):
        is_local_src = type(inode_path) == str
        is_local_dst = type(context.args[1]) == str

        ctxs = {
            (True, True): LocalPushContext,
            (True, False): LocalRemotePushContext,
            (False, True): RemoteLocalPushContext,
            (False, False): RemotePushContext,
        }
        return ctxs[(is_local_src, is_local_dst)](
            context, fs_binding, inode_path, source)

class LocalPullContext(AbstractPullContext):
    def check_path_exists(self):
        if not os.path.exists(self.fpath):
            raise Exception("path doesn't exist %s" % self.fpath)

    def get_inode_path_desc(self):
        gtype = os.path.isfile(self.fpath) and "file" or "folder"
        path2 = "%s://%s" % (gtype, self.fpath)
        return path2

    def read(self):
        with open(self.fpath, "r") as f:
            return f.read()

    def read_folder(self):
        return os.listdir(self.fpath)

    def do_pull(self, path):
        self.set_path(os.path.join(self.fpath, path))
        return self.fs_binding.open_inode(self)

class RemotePullContext(AbstractPullContext):
    def __init__(self, context, fs_binding):
        AbstractPullContext.__init__(self, context, fs_binding)

        
    def clone(self, args=None, deep=False):
        res = AbstractPullContext.clone(self, args)
        res.fpath = copy.deepcopy(self.fpath)
        # ugly as hell...
        if not args:
            res.args[0] = res.fpath
        return res

    def set_path(self, path):
        self.fpath = path
        self.args[0] = path

    def check_path_exists(self):
        # maybe should implement
        pass

    def get_inode_path_desc(self):
        is_file = self._exec_remote(
            self.fpath,
            "test -f %s && echo 1 || echo 0" % self.fpath["path"])[
                "out"][0] == '1'
        gtype = is_file and "file" or "folder"
        path2 = "%s://%s" % (gtype, self.fpath["path"])
        return path2

    def read(self):
        return "\n".join(self._exec_remote(
            self.fpath, "cat %s" % self.fpath["path"])["out"])

    def read_folder(self):
        return [i for i in self._exec_remote(
            self.fpath, "ls %s" % self.fpath[
            "path"])["out"] if i]

    def do_pull(self, path):
        self.fpath["path"] = "%s/%s" % (self.fpath["path"], path)
        self.args[0] = self.fpath
        return self.fs_binding.open_inode(self)

    def clean_up(self):
        pass


class LocalPushContext(AbstractPushContext):
    def write(self, data):
        return self._write_local(data)

    def create_folder(self):
        return self._create_folder_local()

    def write_from_path(self):
        return self._write_from_path_local()

    def write_folder_from_path(self):
        return self._write_folder_from_path_local()

    def do_push(self, path_suffix, source):
        return self._do_push_local(path_suffix, source)

class RemotePushContext(AbstractPushContext):
    def write(self, data):
        return self._write_remote(data)

    def create_folder(self):
        return self._create_folder_remote()

    def write_from_path(self):
        raise Exception("not implemented")

    def write_folder_from_path(self):
        raise Exception("not implemented")

    def do_push(self, path_suffix, source):
        return self._do_push_remote(path_suffix, source)


class RemoteLocalPushContext(AbstractPushContext):
    def __init__(self, *args):
        raise Exception("not implemented")

    def write(self, data):
        return self._write_local(data)

    def create_folder(self):
        return self._create_folder_local()

    def write_from_path(self):
        return self._write_from_path_local()

    def write_folder_from_path(self):
        return self._write_folder_from_path_local()

    def do_push(self, path_suffix, source):
        return self._do_push_local(path_suffix, source)

class LocalRemotePushContext(AbstractPushContext):
    def write(self, data):
        return self._write_remote(data)

    def create_folder(self):
        return self._create_folder_remote()

    def write_from_path(self):
        return self._write_from_path_remote()

    def write_folder_from_path(self):
        return self._write_folder_from_path_remote()

    def do_push(self, path_suffix, source):
        return self._do_push_remote(path_suffix, source)
    

class FsBinding(object):

    def __init__(self, prefix="", root_cobj=None):
        self.prefix = prefix
        self.re_cache = {}
        self.root_cobj = root_cobj and root_cobj or self

    def get_ftypes(self, context):
        return [
            ["^file://.*~$", "ignored"],
            ["^file://.*\\.txt$", "text"],
            ["^file://.*\\.cfg$", "text"],
            ["^file://.*\\.yml$", "yaml"],
            ["^file://.*\\.yaml$", "yaml"],
            ["^file://.*\\.json$", "json"],
            ["^file://.*\\.xml$", "xml"],
            ["^file://.*$", "closed_file"],
            ["^folder://.*$", "closed_folder"],
        ]

    def get_handlers(self, context):
        def do_format(r):
            res = {}
            for k,v in r.iteritems():
                res[k] = [json.dumps(["_fcall", "%s%s" %
                                      (self.prefix, i.__name__)])
                          for i in v]
            return res
        res = {
            "ignored": [self.pull_ignored, self.push_ignored],
            "text": [self.pull_text, self.push_text],
            "yaml": [self.pull_yaml, self.push_yaml],
            "json": [self.pull_json, self.push_json],
            "xml": [self.pull_xml, self.push_xml],
            "closed_file": [self.pull_closed_file,
                            self.push_closed_file],
            "closed_folder": [self.pull_closed_folder,
                              self.push_closed_folder],
            "open_folder": [self.pull_open_folder,
                            self.push_open_folder]
        }
        return do_format(res)

    def get_defaults(self, context):
        return {
            "ftypes": self.get_ftypes(context),
            "handlers": self.get_handlers(context),
        }

    ################### file handlers
    
    # - hcontext is subtype of AbstractHandlerContext which provides
    #   layer to communicate with underlying file system
    # - a handler is expected to return dictionary; usually, it will
    #   have "contents" field; but any set of fields is ok as long
    #   as push/pull is complementary (push needs to understand what
    #   pull wrote in the dictionary)
    # - handler can return None as well
    
    def push_ignored(self, hcontext):
        return None
        
    def push_text(self, hcontext):
        hcontext.write("\n".join(hcontext.source["contents"]))
        
    def push_yaml(self, hcontext):
        hcontext.write(yaml.dump(hcontext.source["contents"]))

    def push_json(self, hcontext):
        hcontext.write(json.dumps(hcontext.source["contents"]))

    def push_xml(self, hcontext):
        def unparse_tree(e):
            if type(e) == str:
                return e
            contents = "".join([unparse_tree(i) for i in e["c"]])
            attribs = " ".join(['%s="%s"' % (k, v) for k,v in e["a"].iteritems()])
            if attribs:
                attribs = " " + attribs
            d = {
                "tag": e["_t"],
                "attribs": attribs,
                "contents": contents
            }
            return "<%(tag)s%(attribs)s>%(contents)s</%(tag)s>" % d
        hcontext.write(unparse_tree(hcontext.source["contents"]))

    def push_closed_file(self, hcontext):
        hcontext.write_from_path()

    def push_closed_folder(self, hcontext):
        hcontext.write_folder_from_path()

    def push_open_folder(self, hcontext):
        hcontext.create_folder()
        for k,v in hcontext.source["contents"].iteritems():
            hc2 = hcontext.clone()
            hc2.do_push(k, v)
        
    def pull_ignored(self, hcontext):
        return None
        
    def pull_text(self, hcontext):
        data = hcontext.read()
        res = []
        for i in data.split("\n"):
            if FCall.is_fcall_str(i):
                fcall = FCall(i)
                res.append(fcall.get_fcall_arr())
            else:
                res.append(i)
        return {
            "contents": res
        }

    def pull_yaml(self, hcontext):
        return {
            "contents": yaml.load(hcontext.read())
        }

    def pull_json(self, hcontext):
        return {
            "contents": json.loads(hcontext.read())
        }
            
    def pull_xml(self, hcontext):
        # TODO: elemtree offers only limited support for parsing
        # xml declaration tag (<?xml ...?>); probably need to use
        # lxml (also comments are not supported; and namespaces
        # are omitted as well)
        root = ET.fromstring(hcontext.read())
        def parse_tree(t):
            contents = []
            if t.text and t.text.strip():
                contents.append(t.text.strip())
            for i in t:
                contents.append(parse_tree(i))
                if i.tail and i.tail.strip():
                    contents.append(i.tail.strip())
            return {
                "_t": t.tag,
                "a": t.attrib,
                "c": contents
            }
        return {
            "contents": parse_tree(root)
        }

    def pull_closed_file(self, hcontext):
        return {
            "path": hcontext.fpath
        }
    def pull_closed_folder(self, hcontext):
        return {
            "path": hcontext.fpath
        }
    def pull_open_folder(self, hcontext):
        res = {}
        for i in hcontext.read_folder():
            hc2 = hcontext.clone()
            res[i] = hc2.do_pull(i)
        return {
            "contents": res
        }

    ##################### operations with inode

    # Reflects inode (file / folder) in doctree.
    #
    # parameters:
    # arg0: path of file / folder for local or
    #       {
    #         host: <host name / ip address>,
    #         cert_file: <ssh certificate file>,
    #         username: <...>,
    #         path: <path to file / folder>,
    #         opts: {   <- optional
    #           port: <ssh port number>
    #         }
    #       }
    #       for remote
    # arg1: configuration object or path to it in doctree
    #   ftypes: list of [regexp, file_type_name]; these are applied
    #           in given order to
    #           file://path/to/file
    #           or
    #           folder://path/to/folder
    #           until regexp matches, then file type name is found
    #   handlers: dictionary of ftype: [pull_handler, push_handler],
    #           where both handlers are fcalls in string form
    #
    # return:
    # {
    #   path: <==arg0>,
    #   inode: {
    #     ftype: <file / folder type>,
    #     <pull handler fcall result>
    #   }
    # }
    #
    # first recursion is returning metadata structure (path, inode
    # fields); context type is used to check if the call is first
    # one
    def open_inode(self, context):
        def is_match(p, path_desc):
            if not p in self.re_cache:
                self.re_cache[p] = re.compile(p)
            return self.re_cache[p].match(path_desc)
        path = context.args[0]
        cfg = context.args[1]
        if type(cfg) == str:
            p = Path(cfg, context.doc)
            cfg = p.get_val(context.doc)
            
        is_first_call = not isinstance(context,
                                       AbstractHandlerContext)

        if is_first_call:
            context = AbstractPullContext.create_pull_handler(
                context, self)

        context.check_path_exists()
        path_desc = context.get_inode_path_desc()
        ftype = None
        for p,ft in cfg["ftypes"]:
            if is_match(p, path_desc):
                ftype = ft
                break

        if not ftype:
            raise Exception("undefined type for %s" % path_desc)
                
        if not ftype in cfg["handlers"]:
            raise Exception("unknown type for %s, %s" % (path_desc,
                                                         ftype))
        fcall = FCall(cfg["handlers"][ftype][0])
        fcall.add_params(*context.args)
        res = fcall.do_exec(self.root_cobj, context)
        if res:
            res["ftype"] = ftype
        if is_first_call:
            context.clean_up()
            return {
                "inode": res,
                "path": path
            }
        return res

    # Reflects doctree contents as file/folder tree.
    #
    # parameters:
    # arg0: path in doctree of fs reflection, with metadata, or
    #       object to reflect itself
    # arg1: file path for local or
    #       {
    #         host: <host name / ip address>,
    #         cert-file: <ssh certificate file>,
    #         username: <...>
    #         path: <path to file / folder>
    #       }
    #       for remote
    # arg2: configuration object or path to it in doctree
    #   ftypes: list of [regexp, file_type_name]; these are applied
    #           in given order to
    #           file://path/to/file
    #           or
    #           folder://path/to/folder
    #           until regexp matches, then file type name is found
    #   handlers: dictionary of ftype: [pull_handler, push_handler],
    #           where both handlers are fcalls in string form
    #
    # return: None
    #
    # additional effects: creates file system subtree from arg0
    def save_inode(self, context):
        source_path = context.args[0]
        inode = type(source_path) == str and context.getv(
            source_path) or source_path

        target_path = context.args[1]
        cfg = context.args[2]
        if type(cfg) == str:
            p = Path(cfg, context.doc)
            cfg = p.get_val(context.doc)

        is_first_call = not isinstance(context,
                                       AbstractHandlerContext)

        if is_first_call:
            # inode["path"] is important only if there are closed
            # files/folders in the structure
            context = AbstractPushContext.create_push_handler(
                context, self, inode.get("path", ""),
                inode["inode"])
            inode = inode["inode"]            
        
        if not inode:
            return
        if not "ftype" in inode:
            raise Exception("undefined type for %s" % source_path)
            
        ftype = inode["ftype"]
        if not ftype in cfg["handlers"]:
            raise Exception("unknown type for %s, %s" % (source_path,
                                                         ftype))

        fcall = FCall(cfg["handlers"][ftype][1])
        fcall.add_params(inode, target_path, cfg)
        res = fcall.do_exec(self.root_cobj, context)
        if is_first_call:
            context.clean_up()
        return res

    # executes command locally
    #
    # parameters:
    # arg0: command in list format (ex. [ls, -al, /tmp])
    # arg1: options
    #   allow_rm_rf_asterisk: to not check for dangerous rm -rf *
    #          type of operations
    def exec_local(self, context):
        cmd = context.args[0]
        opts = len(context.args) > 1 and context.args[1] or {}
        cwd = opts.get("cwd", None)
        if (len(cmd) >= 3 and cmd[0] == "rm" and
            ("-rf" in cmd or "-r" in cmd)
            and "*" in "".join(cmd) and
            not "allow_rm_rf_asterisk" in opts):
            raise Exception("wildcard * not allowed with rm -r, use allow_rm_rf_asterisk in opts dictionary to bypass this check")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=cwd)
        # TODO: support output for long-running things would be cool
        out, err = p.communicate()
        if p.returncode:
            raise PukalaFsException(cmd, cwd, p.returncode, out, err)
        out = out and out or ""
        err = err and err or ""
        out = out.split("\n")
        err = err.split("\n")
        return {
            "cmd": cmd,
            "cwd": cwd,
            "out": out,
            "err": err
        }

    # executes list of bash commands; this is just a basic
    # implementation
    def exec_local_batch(self, context):
        cmd = context.args[0]
        opts = len(context.args) > 1 and context.args[1] or {}
        cwd = opts.get("cwd", None)
        p = subprocess.Popen(["bash"], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, cwd=cwd)

        p.stdin.write("\n".join(cmd))
        p.stdin.close()

        def read_out(ff):
            out = []
            while True:
                zz = ff.read()
                if not zz:
                    break
                out.append(zz)
            out = "\n".join(out).split("\n")
            return out
        out = read_out(p.stdout)
        err = read_out(p.stderr)
        p.terminate()

        if p.returncode:
            raise PukalaFsException(cmd, cwd, p.returncode, out, err)
        return {
            "cmd": cmd,
            "cwd": cwd,
            "out": out,
            "err": err
        }

    # executes list of bash commands remotely; this is just a basic
    # implementation
    def exec_remote_batch(self, context):
        args = copy.copy(context.args)
        args[3] = " && ".join(args[3])
        if len(args) < 5:
            args.append({})
        args[4]["pseudo-tty"] = True
        return self.exec_remote(context.clone(args))
            
    def send_file(self, context):
        a_file, cert_file, username, host, target_folder = context.args[:5]
        opts = len(context.args) > 5 and context.args[5] or {}
        port = str(opts.get("port", 22))
        recursive = opts.get("recursive", False)
        cmd = ['scp', '-oStrictHostKeyChecking=no']

        if port != 22:
            cmd += ['-P', port]

        if recursive:
            cmd += ["-r"]
            
        cmd += ['-i', cert_file, a_file, "%s@%s:%s" % (
                   username, host, target_folder)]
        return self.exec_local(context.clone([cmd]))

    def get_file(self, context):
        a_file, cert_file, username, host, target_folder = context.args[:5]
        opts = len(context.args) > 5 and context.args[5] or {}
        port = str(opts.get("port", 22))

        cmd = ['scp', '-oStrictHostKeyChecking=no', '-P', port,
               '-i', cert_file,
               "%s@%s:%s" % (username, host, a_file), target_folder]
        return self.exec_local(context.clone([cmd]))

    # executes command remotely
    #
    # parameters:
    # arg0: certificate file
    # arg1: username
    # arg2: host
    # arg3: command in string format
    # arg4: options
    #   port: default 22
    def exec_remote(self, context):
        cert_file, username, host, cmd0 = context.args[:4]
        opts = len(context.args) > 4 and context.args[4] or {}
        port = str(opts.get("port", 22))
        pseudo_tty = opts.get("pseudo-tty", False)
        cmd = ["ssh"]
        if port != "22":
            cmd += ['-p', port]
        if pseudo_tty:
            cmd += ["-T"]
        cmd += ['-i', cert_file,
               "%s@%s" % (username, host), cmd0]
        return self.exec_local(context.clone([cmd]))
