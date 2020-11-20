import subprocess
from dragonfly import *

from supporting import utils

def openFile(command):
    subprocess.Popen(command)

class OpenFilesRule(MappingRule):
    mapping = {
        "file voice working": Function(openFile, command=r'notepad "C:\Users\hawk\Desktop\voice_working.txt"'),
        "file daily tasks": Function(openFile, command=r'"C:\Program Files\Windows NT\Accessories\wordpad.exe" "D:\Google Drive\working\daily tasks.rtf"'),
    }
    extras = [Dictation("text"),
              ]
    defaults = {"text":None}


open_files_grammar = Grammar("Open certain files")
open_files_grammar.add_rule(OpenFilesRule())


open_files_grammar.load()

def unload():
    global open_files_grammar
    open_files_grammar = utils.unloadHelper(open_files_grammar, __name__)