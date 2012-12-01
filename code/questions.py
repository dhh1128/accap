from textui.ansi import *
from textui.colors import *
from textui.getch import *
from textui.prompt import *

def _strip_and_lower_case(txt):
    return txt.strip().lower()

def which_mode(answers):
    key = 'type of deployment'
    dflt = 'cloud'
    answer = prompt('Type of deployment', 'cloud|hpc', 
                    default=answers.get(key, dflt),
                    normfunc=_strip_and_lower_case,
                    acceptfunc=lambda x: re.match('cloud|hpc', x))
    answers[key] = answer
    
first = which_mode    
    