import glob, os, shutil, log_to_file, datetime, time
from os import path
from tkinter import *
from tkinter import messagebox
from program_list import ProgramList

class programs_updater():
    """Class is used to maintain updating operations and logging it results."""


    def __init__(self):
        #define variables
        self.now = datetime.datetime.now()
        self.success = 'success'
        self.error = 'error'
        self.fail_message = False
       
        #current directory variable to create log files later
        self.cwd = os.getcwd()

        #get settings from file to copy from path1 to path2
        with open('settings.upd', 'r') as settings_file:
            settings = settings_file.readlines()
     
        #initialize path variables with data from settings file
        for line in settings:
            setting = line.rstrip('\n')
            if '#' in line:
                continue
            
            if 'dirpath_to_update' in line:
                self.dirpath_to_update = setting[setting.index('=') + 1:]
       
            elif 'dirpath_from_update' in line:
                self.dirpath_from_update = setting[setting.index('=') + 1:]

            elif 'files_update_ext' in line:
                self.update_ext = setting[setting.index('=') + 1:].split(';')
                
            elif 'network_path' in line:
                self.network_path = setting[setting.index('=') + 1:]

            elif 'user' in line:
                self.user = setting[setting.index('=') + 1:]

            elif 'password' in line:
                self.password = setting[setting.index('=') + 1:]

            elif 'fail_message' in line and 'True' in line:
                self.fail_message = True
                

        self.message_error_log = '\t FAILED!\t FILE IS BUSY! USER DECLINED'
        self.message_success_log = '\tis copied from:\t' + self.dirpath_from_update + \
                                   '\tto:\t' + self.dirpath_to_update


    #update file function
    def updateFile(self, from_dir, to_dir, fileName):
        """Copies the file, saving metadata and timestamps.

            Args:
            from_dir -- Path from updates will be copied.
            to_dir -- Path to updates will be copied.
            fileName -- Name of file which will be copied.
        """

        #copy file with seving metadata
        shutil.copy2(path.join(from_dir, fileName), to_dir, follow_symlinks = False)

        #write success log
        self.write_log(self.success, fileName, self.message_success_log)

        #print info to console(for debug)
        print(self.now.strftime("%Y-%m-%d %H:%M:%S ") + fileName + '\tis copied from:\t' + \
              from_dir + '\tto:\t' + to_dir)


    #call dialog box for user choise if he|she wants to update right now
    def callback(self, process_name):
        """Creates the prompt dialog for user to decide if one wants to update
            the app which is running now. Closes running process to update file.

            Args:
            process_name -- Must be a str. Name of currently running process.
                            Used to display userfriendly program name in prompt.
                
        """
        
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
        """Writes log to a file.

            Args:
            log_type -- Used as name of log file.
            file_name -- Name of file, which was (or not) updated to write it to the log.
            message -- Message which will be written to the log (e.g. "successfully updated")
        """
        
        log_to_file.write_log(log_type, self.now.strftime("%Y-%m-%d %H:%M:%S ") + \
                                  file_name + message)
    
    
    #main method which runs a script
    #creates list of files to update
    def update(self):
        """Gathers all files with certain extentions from the pathes from update and to update.
            Checks if file need to be updated and if there are all files are in working direcroty.
            Tries to update all files. Calls a prompt dialog if file needs to be updated but is
            busy now.
        """
        
        #create two lists to compare files in path1 and path2
        files_to_update = []
        files_from_update = []
        updating_list = []
    
        os.chdir(self.dirpath_to_update)
        
        for ext in self.update_ext:
            for file in glob.glob(ext):
                files_to_update.append(file)

        os.chdir(self.dirpath_from_update)
        
        for ext in self.update_ext:
            for file in glob.glob(ext):
                files_from_update.append(file)

        #compare and fill the files to update list
        for file in files_from_update:

            #if modifying time of file 1 is greather than file 2 - need update
            if (file in files_to_update) and \
               (path.getmtime(path.join(self.dirpath_from_update, file)) > path.getmtime(path.join(self.dirpath_to_update, file))):
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


    #checks network path for availability    
    def check_disk(self):
        """Checks if the disk with updates is available. Tries to connect if not."""
        
        disk_add = r"net use " + self.dirpath_from_update[:2] + " " + self.network_path + " /persistent:yes"
        disk_add_with_user = r"net use " + self.dirpath_from_update[:2] + " " + self.network_path + " /user:" + self.user + " " + self.password + " /persistent:yes"

        #for case if another user acc is used for connection
        if not os.path.exists(self.dirpath_from_update):
            os.system(disk_add)
        else:
            return True
        
        #for case if there is no user acc is used for connection
        if not os.path.exists(self.dirpath_from_update):
            os.system(disk_add_with_user)
        else:
            return True
        
        #if can't connect path
        if not os.path.exists(self.dirpath_from_update) and self.fail_message:
            root = Tk()
            root.attributes("-topmost", True)
            root.withdraw()
            messagebox.showinfo('Проверка доступа по сети', \
                                'Не получилось подключиться к сетевому диску.\n' + \
                                'Обновление программ невозможно!\n' + \
                                'Проверьте соединение с Киевом!')
            return False


        
