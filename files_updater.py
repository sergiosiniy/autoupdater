import glob, os, shutil, log_to_file
from os import path

success='success_log'
error='error_log'
cwd=os.getcwd()

setings_file=open('setings.upd','r')
setings=setings_file.readlines()
setings_file.close()


for line in setings:
    seting=line.rstrip('\n').split('=')

    if seting[0]=='dirpath_to_update':
        dirpath_to_update=seting[1]
    elif seting[0]=='dirpath_from_update':
        dirpath_from_update=seting[1]      
        
def update():
    
    os.chdir(dirpath_to_update)

    files_to_update=[]
    files_from_update=[]
    updating_list=[]

    for file in glob.glob('*.exe'):
        files_to_update.append(file)

    os.chdir(dirpath_from_update)

    for file in glob.glob('*.exe'):
        files_from_update.append(file)


    #print(files_to_update)
    #print(files_from_update)

    for file in files_from_update:
        if (file in files_to_update) and \
        (path.getctime(dirpath_from_update+'\\'+file)>\
         path.getctime(dirpath_to_update+'\\'+file)):
            updating_list.append(file)
        elif not file in files_to_update:
            updating_list.append(file)

    os.chdir(cwd)

    for file in updating_list:
        try:
            shutil.copy(dirpath_from_update+'\\'+file, \
                        dirpath_to_update,follow_symlinks=True)
            log_to_file.write_log(success,file+'\tis copied from:\t'+ \
                       dirpath_from_update+'\tto:\t'+dirpath_to_update)
            print(file+'\tis copied from:\t'+dirpath_from_update+ \
                  '\tto:\t'+dirpath_to_update)
            
        except IOError:
            log_to_file.write_log(error,file+'\t FAILED!\t FILE IS BUSY!')
            print(file+'\t FAILED!\t FILE IS BUSY!')
        

    if len(updating_list)==0:
        print('All is up to date.')


