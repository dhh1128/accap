from textui.ansi import *
from textui.colors import *
from textui.getch import *
from textui.prompt import *

def _strip_and_lower_case(txt):
    return txt.strip().lower()

def _norm_list(txt):
    txt = re.sub('[,;]', ' ', _strip_and_lower_case(txt))
    txt = re.sub(' +', ' ', txt)
    items = txt.split(' ')
    x = {}
    for i in items:
        x[i] = 1
    items = x.keys()
    items.sort()
    txt = ','.join(items)
    return txt

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
    return num_hypervisors
    
def num_hypervisors(answers):
    answer = fancy_prompt('Number of hypervisors', '[1-9][0-9]{0,4}', answers)
    return num_new_jobs_per_hour

def num_new_jobs_per_hour(answers):
    answer = fancy_prompt('Number of new jobs per hour', '[1-9][0-9]{0,3}', answers)
    return which_rm
    
def which_rm(answers):
    answer = fancy_prompt('Which RMs', '(slurm|torque|fifo)([, ]+(slurm|torque|fifo))*', answers, normfunc=_norm_list)

first = which_mode    
    