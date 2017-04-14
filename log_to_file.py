def write_log(logname,string):
    """Creates log dile and appends log entries to it.

        Args:
        logname -- Is used as name of log file to create or append.
    """

    with open(logname + '.log','a') as log:
            log.write(string+'\n')            

