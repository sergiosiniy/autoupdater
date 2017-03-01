import glob, os, shutil, log_to_file, datetime
from os import path
from tkinter import *
from tkinter import messagebox
from program_list import ProgramList

#define variables
now=datetime.datetime.now()
success='success_log'
error='error_log'

#current directory variable to create log files later
cwd=os.getcwd()

#get settings from file to copy from path1 to path2
setings_file=open('setings.upd','r')
setings=setings_file.readlines()
setings_file.close()

#initialize path variables with data from settings file
for line in setings:
    seting=line.rstrip('\n').split('=')

    if seting[0]=='dirpath_to_update':
        dirpath_to_update=seting[1]
    elif seting[0]=='dirpath_from_update':
        dirpath_from_update=seting[1]

#update file function
def updateFile(from_dir,to_dir, fileName):
    #copy file with seving metadata
    shutil.copy2(dirpath_from_update+'\\'+fileName,dirpath_to_update,follow_symlinks=False)
    #write to success log
    log_to_file.write_log(success,now.strftime("%Y-%m-%d %H:%M:%S ")+fileName+'\tis copied from:\t'+\
                          dirpath_from_update+'\tto:\t'+dirpath_to_update)
    #print info to console
    print(now.strftime("%Y-%m-%d %H:%M:%S ")+fileName+'\tis copied from:\t'+\
          dirpath_from_update+'\tto:\t'+dirpath_to_update)

#call dialog box for user choise if he|she wants to update right now
def callback(processName):
    #the askyesno function opens empty tk window, so we need explicitly call and close it
    Tk().withdraw()
    programlist = ProgramList()
    programName = programlist.getProgramName(processName)
    if messagebox.askyesno('Обновление \"%s\"' % (programName), \
                           'Хотите обновить программу \"%s\" сейчас?\nПрограмма будет закрыта!'\
                           % (programName)):
        run=True
        os.system('taskkill /im %s' % (processName))
        while run:
            
            processes=os.popen('tasklist').read()
            if not processName in processes:
                run=False
                updateFile(dirpath_from_update,dirpath_to_update,processName)        
        
    else:
        messagebox.showinfo('Программа \"%s\"' % (programName), \
                 'Программа не будет обновлена.\nНе забудьте обновить позже!')
        log_to_file.write_log(error, \
                              now.strftime("%Y-%m-%d %H:%M:%S ")+\
                              processName+'\t FAILED!\t FILE IS BUSY! USER DECLINED')
        print(now.strftime("%Y-%m-%d %H:%M:%S ")+\
              processName+'\t FAILED!\t FILE IS BUSY!')

#main method which runs a script
#creates list of files to update
def update():

    #create two lists to compare files in path1 and path2
    

    files_to_update=[]
    files_from_update=[]
    updating_list=[]

    os.chdir(dirpath_to_update)
    
    for file in glob.glob('*.exe'):
        files_to_update.append(file)

    os.chdir(dirpath_from_update)

    for file in glob.glob('*.exe'):
        files_from_update.append(file)

    #compare and fill the files to update list
    for file in files_from_update:

        #if modifying time of file 1 is greather than file 2 - need update
        if (file in files_to_update) and \
           (path.getmtime(dirpath_from_update+'\\'\
            +file)>path.getmtime(dirpath_to_update+'\\'+file)):
            updating_list.append(file)
            
        elif not file in files_to_update:
            updating_list.append(file)

    #ch dir for writing logs into
    os.chdir(cwd)

    
   
    for file in updating_list:
        try:
            updateFile(dirpath_from_update,dirpath_to_update,file)
        except IOError:
            callback(file)

    if len(updating_list)==0:
        print('All is up to date.')

    
