import os
import sys
import ConfigParser
import optparse

import questions

def read(fname):
    answers = {}
    if fname:
        cfg = ConfigParser.RawConfigParser()
        f = open(fname, 'r')
        cfg.readfp(f)
        for name, value in cfg.items('answers'):
            answers[name] = value
    return answers

def backup(fname):
    if os.path.isfile(fname):
        bak = fname + '.bak'
        n = 2
        while os.path.isfile(bak):
            bak = bak[0:bak.rfind('.')] + '.bak' + str(n)
            n += 1
        os.rename(fname, bak)
        print('Moved old %s to %s.' % (fname, bak))

def display(data):
    for key, valmap in data.items():
        print('[%s]' % key)
        for name, value in valmap.items():
            print('%s=%s' % (name, value))
        print

def write(fname, answers, predictions, recommendations):
    data = {'answers': answers, 'predictions': predictions, 'recommendations': recommendations}
    if not fname:
        display(data)
    else:
        cfg = ConfigParser.RawConfigParser()
        print data
        for key, valmap in data.items():
            cfg.add_section(key)
            for name, value in valmap.items():
                cfg.set(name, value)
        new = fname + '.new'
        f = open(new, 'w')
        cfg.write(f)
        f.close()
        backup(fname)
        os.rename(new, fname)
        print('Saved answers, predictions, and recommendations to %s.' % fname)
        
def interact(answers):
    next_q = questions.first
    while next_q:
        next_q = next_q(answers)
        
def predict(answers):
    viewPoint_memory = 1500
    MWS_memory = 700
    httpd_memory = 95.4
    mongod_memory = 63.7
    msmd_memory = 20
    number_of_jobs = int(answers['number of jobs'])
    MAM_diskspace = round((number_of_jobs * 2000) * .000001,2)
    torque_memory =  number_of_jobs * .001
    moab_memory = number_of_jobs * 1
    predictions = {}
    ram_total = round(((moab_memory + torque_memory + MWS_memory + httpd_memory + mongod_memory + msmd_memory + viewPoint_memory) * .001),1) + .1
    predictions['RAM required GB'] = ram_total
    predictions['Diskspace per year used '] = " %s GB" % (float(answers['number of new jobs per hour']) * .017520)
    
    return predictions

def recommend(answers, predictions):
    recommendations = {}
    recommendations['Machines recommended '] = " %s machines" % (((int(answers['number of jobs']) / 10000) + 1)  + 2)
    recommendations['Memory recommended '] = " %s GB of memory" % float(predictions['RAM required GB'])
    return recommendations
        
def main(options):
    answers = read(options.read)
    interact(answers)
    predictions = predict(answers)
    recommendations = recommend(answers, predictions)
    write(options.write, answers, predictions, recommendations)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-r", "--read", dest="read",
                      help="read initial answers from file", metavar="FILE")
    parser.add_option("-w", "--write", dest="write",
                      help="write answers, predictions, and recommendations to file", metavar="FILE")    
    parser.add_option("--no-color", dest="nocolor", default=False, action="store_true",
                      help="don't use ansi escapes to prettify output", metavar="FILE")    
    (options, args) = parser.parse_args()
    main(options)
