def write_log(logname,string):

    with open(logname + '.log','a') as log:
            log.write(string+'\n')            

