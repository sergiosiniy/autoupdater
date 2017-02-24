def write_log(logname,string):

    if logname == 'error_log':
        with open('error_log.log','a') as log:
            log.write(string+'\n')
           
    elif logname == 'success_log':        
        with open('success_log.log','a') as log:
            log.write(string+'\n')
            

