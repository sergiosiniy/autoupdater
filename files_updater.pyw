import glob, os, shutil, log_to_file, datetime, time
from os import path
from tkinter import *
from tkinter import messagebox
from program_list import ProgramList

class programs_updater():


    def __init__(self):
        #define variables
        self.now = datetime.datetime.now()
        self.success = 'success'
        self.error = 'error'
       

        #current directory variable to create log files later
        self.cwd = os.getcwd()

        #get settings from file to copy from path1 to path2
        settings_file = open('settings.upd', 'r')
        settings = settings_file.readlines()
        settings_file.close()

        #initialize path variables with data from settings file
        for line in settings:
            setting = line.rstrip('\n')
            if 'dirpath_to_update' in line:
                self.dirpath_to_update = setting[setting.index('=') + 1:]
       
            elif 'dirpath_from_update' in line:
                self.dirpath_from_update = setting[setting.index('=') + 1:]

        self.message_error_log = '\t FAILED!\t FILE IS BUSY! USER DECLINED'
        self.message_success_log = '\tis copied from:\t' + self.dirpath_from_update + \
                                   '\tto:\t' + self.dirpath_to_update

    #update file function
    def updateFile(self, from_dir, to_dir, fileName):

        #copy file with seving metadata
        shutil.copy2(from_dir + '\\' + fileName, to_dir, follow_symlinks = False)

        #write success log
        self.write_log(self.success, fileName, self.message_success_log)

        #print info to console(for debug)
        print(self.now.strftime("%Y-%m-%d %H:%M:%S ") + fileName + '\tis copied from:\t' + \
              from_dir + '\tto:\t' + to_dir)


    #call dialog box for user choise if he|she wants to update right now
    def callback(self, process_name):
        #the askyesno function opens empty tk window, so we need explicitly call and close it
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        
        program_list = ProgramList()
        program_name = program_list.getProgramName(process_name)
        if messagebox.askyesno('Обновление \"%s\"' % (program_name), \
                               'Хотите обновить программу \"%s\" сейчас?\nПрограмма будет закрыта!'\
                               % (program_name)):
            run = True
            count = 0
            os.system('taskkill /im %s' % (process_name))
            while run:
                time.sleep(0.5)
                processes = os.popen('tasklist').read()
                if not process_name in processes:
                    run = False
                    self.updateFile(self.dirpath_from_update, self.dirpath_to_update, process_name)

                if count == 3:
                    os.system('taskkill /im %s' % (process_name))
                    count = 0

                count += 1
            messagebox.showinfo('Обновление \"%s\"' % (program_name), \
                                'Программа \"%s\" успешно обновлена.\nМожно продолжать работу.'\
                                % (program_name))    
        else:
            messagebox.showinfo('Программа \"%s\"' % (program_name), \
                     'Программа не будет обновлена.\nНе забудьте обновить позже!')
            
            #write to error log
            self.write_log(self.error, process_name, self.message_error_log)
            
            #print to console (used for debug)
            print(self.now.strftime("%Y-%m-%d %H:%M:%S ") + \
                  process_name + '\t FAILED!\t FILE IS BUSY!')


    #write message to the log
    def write_log(self,log_type,file_name,message):
        log_to_file.write_log(log_type, self.now.strftime("%Y-%m-%d %H:%M:%S ") + \
                                  file_name + message)
    
    
    #main method which runs a script
    #creates list of files to update
    def update(self):
    
        #create two lists to compare files in path1 and path2
        files_to_update = []
        files_from_update = []
        updating_list = []
    
        os.chdir(self.dirpath_to_update)
        
        for file in glob.glob('*.exe'):
            files_to_update.append(file)

        os.chdir(self.dirpath_from_update)

        for file in glob.glob('*.exe'):
            files_from_update.append(file)

        #compare and fill the files to update list
        for file in files_from_update:

            #if modifying time of file 1 is greather than file 2 - need update
            if (file in files_to_update) and \
               (path.getmtime(self.dirpath_from_update + '\\' \
                + file) > path.getmtime(self.dirpath_to_update + '\\' + file)):
                updating_list.append(file)
                
            elif not file in files_to_update:
                updating_list.append(file)

        #ch dir for writing logs into
        os.chdir(self.cwd)  
       
        for file in updating_list:
            try:
                self.updateFile(self.dirpath_from_update, self.dirpath_to_update, file)
            except IOError:
                self.callback(file)
                continue

        if len(updating_list) == 0:
            print('All is up to date.')

        
