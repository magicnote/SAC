import sublime_plugin
import sublime
import subprocess
import os
import json

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))

DEBUG = False

class SAC(sublime_plugin.EventListener):

    def __init__(self):
        if DEBUG: print("initializing SAC plugin")
 
    def on_query_completions(self, view, prefix, locations):
 
        if DEBUG: print("SAC: running completion query '{0}'".format(prefix))
        words = []

        buf = prefix.split('->')
        if DEBUG: print("SAC: split {0}".format(buf))

        if len(buf) <= 1 : 
            return words;

        cls = self.resolvePHPClass(view, buf[0])
        methods =   self.lint(cls)

        for method in methods:
            # 第二个参数 $存在变量解析问题,需转义
            words.append([self.prefix(buf[0], method), self.prefix(buf[0], method, True)])
        
        
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
            word = cls[1].strip()
            if DEBUG: print("SAC: class {0}  found".format(word))
            return word

    def lint(self, cls):
        sac_path = ''.join(['php "', PLUGIN_DIR , '\\sac.php', '" ', cls]) 
        p = subprocess.Popen(sac_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p.communicate()[0]   
        if DEBUG: print("SAC: script output \n {0}  ".format(output))
        return json.loads(str(output, 'utf8'))

    def prefix(self, prefix, method, safe = False):
        buf = [prefix, '->' ,method]
        if safe : buf.insert(0, '\\')
        return ''.join(buf)

   