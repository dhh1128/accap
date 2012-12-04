from textui.ansi import *
from textui.colors import *
from textui.getch import *
from textui.prompt import *

def _strip_and_lower_case(txt):
    return txt.strip().lower()

def fancy_prompt(q, regex, answers, dflt=None, normfunc=None, acceptfunc=None, comment=None):
    key = q.strip().lower()
    if not normfunc:
        normfunc = _strip_and_lower_case
    if (not acceptfunc) and regex:
        acceptfunc = lambda val: re.match(regex, val)
    if comment:
        print(comment)
        print('')
    answer = prompt(q, regex, default=answers.get(key, dflt),
                    normfunc=normfunc, acceptfunc=acceptfunc)
    answers[key] = answer
    return answer

def which_mode(answers):
    answer = fancy_prompt('Type of deployment', 'cloud|hpc', answers)
    return num_nodes
    
def num_nodes(answers):
    answer = fancy_prompt('Number of nodes', '[1-9][0-9]{0,4}', answers)
    
first = which_mode    
    