import sublime_plugin
import sublime
import subprocess
import os
import json

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))

DEBUG = True

class SAC(sublime_plugin.EventListener):

    def __init__(self):
        if DEBUG: print("initializing SAC plugin")
 
    def on_query_completions(self, view, prefix, locations):
    
        words = []

        buf = prefix.split('->')
        if DEBUG: print("SAC: split {0}".format(buf))

        if len(buf) <= 1 : 
            return words;

        buf =  '->'.join(buf[0:-1])

        if DEBUG: print("SAC: running completion query '{0}'".format(buf))

        cls = self.resolvePHPClass(view, buf)
        methods =   self.lint(view, cls)

        for method in methods:
            # 第二个参数 $存在变量解析问题,需转义
            words.append([self.prefix(buf, method), self.prefix(buf, method, True)])
        
        if DEBUG: print("SAC: {0} methods found".format(len(words)))

        return words
    
    def resolvePHPClass(self, v, var):
        # 比较low,且不大准确的做法 正则该变量所有的new
        # 取最后一次new 去查找
        pattern = ''.join(['\\', var, '[\s]*=[\s]*new[\s]*([^(;\s]+)'])
        mathes = v.find_all(pattern)

        buf = []

        for position in mathes[::-1]:
            cls = v.substr(position).split('new')
            word = self.resolvePHPClassName(v, cls[1].strip())
            return word

    def resolvePHPClassName(self, v, cls):
        # is contains namespace
        if '\\' == cls[:1]:
            return cls

        # is php native class
        if self.isPHPNativeClass(cls):
            return cls
        
        # find in use or current namespace
        return self.findClassInUse(v, cls)
        
    def findClassInUse(self, v, cls):
        pattern = ''.join(['use([^\r\n]+)', cls, ';'])
        mathes = v.find_all(pattern)

        for position in mathes[::-1]:
            cls = v.substr(position).replace('use', '').replace(';', '')
            word = cls.strip()
            if DEBUG: print("SAC: class {0}  found (use)".format(word))
            return word

        pattern = ''.join(['namespace([^;]+)'])
        mathes = v.find_all(pattern)

        for position in mathes[::-1]:
            return v.substr(position).replace('namespace', '').replace(';', '').strip()

    def isPHPNativeClass(self, cls):
        return False

    def lint(self, view, cls):
        project_path = self.getWorkspace(view)
        sac_path = ''.join(['php "', PLUGIN_DIR , '\\sac.php', '" ', cls, ' "', project_path, '"']) 
        p = subprocess.Popen(sac_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p.communicate()[0]   
        if DEBUG: 
            print("SAC: script input \n {0}  ".format(sac_path))
            print("SAC: script output \n {0}  ".format(output))
        try:
            return json.loads(str(output, 'utf8'))
        except Exception as e:
            return [];


    def prefix(self, prefix, method, safe = False):
        buf = [prefix, '->' ,method]
        if safe : buf.insert(0, '\\')
        return ''.join(buf)

    def getWorkspace(self, v):
        # matches first 
        for folder in v.window().folders():
            if v.file_name().find(folder) != -1:
                return folder
        return None