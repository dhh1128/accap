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

def fancy_prompt(q, regex,  answers, dflt=None, normfunc=None, acceptfunc=None, comment=None,question = None):
    key = q.strip().lower()
    if not normfunc:
        normfunc = _strip_and_lower_case
    if (not acceptfunc) and regex:
        acceptfunc = lambda val: re.match(regex, val)
    if comment:
        writec(YELLOW + comment)
        print('')
   
    answer = prompt(q, regex, default=answers.get(key, dflt),
                    normfunc=normfunc, acceptfunc=acceptfunc,question = question)
    printc(NORMTXT)
    answers[key] = answer
    return answer

  
def which_mode(answers):
    string1 = 'please enter in your deployment'
    string2 = '(cloud|hpc)'
    answer = fancy_prompt('Type of deployment', '(cloud|hpc)', answers, comment = string1, question = string2)
    return num_nodes

def num_nodes(answers):
    string1 = 'please enter in nodes'
    string2 = 'a number between 1 and 100'
    answer = fancy_prompt('Number of nodes', '[1-9][0-9]{0,4}', answers, comment = string1, question = string2)
    return num_hypervisors
    
def num_hypervisors(answers):
    string1 = 'please enter in hypervisors'
    string2 = 'a number between 1 and 10'
    answer = fancy_prompt('Number of hypervisors', '[1-9][0-9]{0,4}', answers, comment = string1, question = string2)
    return num_of_jobs

def num_of_jobs(answers):
    string1 = 'please enter in jobs'
    string2 = 'a number between 1 and 50'
    answer = fancy_prompt('Number of jobs', '[1-9][0-9]{0,3}', answers, comment = string1,question = string2)
    return num_new_jobs_per_hour

    
def num_new_jobs_per_hour(answers):
    string1 = 'please enter in jobs per hour'
    string2 = 'a number between 1 and 50'
    answer = fancy_prompt('Number of new jobs per hour', '[1-9][0-9]{0,3}', answers, comment = string1,question = string2)
    return which_rm
    
def which_rm(answers):
    string1 = 'please enter in RMs'
    string2 = '(slurm|torque|fifo)'
    answer = fancy_prompt('Which RMs', '(slurm|torque|fifo)([, ]+(slurm|torque|fifo))*', answers, normfunc=_norm_list,comment = string1,question = string2)
    
first = which_mode    
    