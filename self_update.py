import glob, os, shutil, log_to_file, datetime

class self_update():
    
    
    def __init__(self):
        #define variables
        self.now = datetime.datetime.now()
        self.success = "success_mupdate"
        self.error = "error_mupdate"

        #current dir
        self.cwd = os.getcwd()

        with open('settings.upd', 'r') as settings_file:
            settings = settings_file.readlines()

        #get path for update modules
        for line in settings:
            if '#' in line:
                continue
            else:
                setting = line.rstrip('\n')
                if 'modules_update_path' in line:
                    self.modules_update_path = setting[setting.index('=')+1:]
                elif 'modules_update_ext' in line:
                    self.modules_ext = setting[setting.index('=')+1:].split(';')


    def update_modules(self):
        if len(self.modules_update_path) > 0:
            update_from = []
            update_to = []
            update_list = []

            for file_ext in self.modules_ext:
                for file in glob.glob(file_ext):
                    update_to.append(file)

            os.chdir(self.modules_update_path)

            for file_ext in self.modules_ext:
                for file in glob.glob(file_ext):
                    update_from.append(file)

            #compare and fill the files to update list
            for file in update_from:

                #if modifying time of file 1 is greather than file 2 - need update
                if (file in update_to) and \
                   (os.path.getmtime(self.modules_update_path + '\\'\
                    +file) > os.path.getmtime(self.cwd + '\\' + file)):
                    update_list.append(file)
                    
                elif not file in update_to:
                    update_list.append(file)
            
            if len(update_list) < 1:
                os.chdir(self.cwd)
                return True
            else:
                os.chdir(self.cwd)

                for file in update_list:
                    try:
                        self.updateFile(self.modules_update_path, self.cwd, file)
                    except IOError:
                        self.write_log(self.error, file, " is not updated!")
                        return False

                return True
        else:
            self.write_log(self.error, 'ERROR!', ' FAILED TO GET UPDATE PATH')
            return False

            
    #update modules
    def updateFile(self, from_dir,to_dir, fileName):
        #copy file with seving metadata
        shutil.copy2(from_dir + '\\' + fileName, to_dir,follow_symlinks = False)
        self.write_log(self.success, fileName, " successfully updated!")

     #write message to the log
    def write_log(self,log_type, file_name,message):
        log_to_file.write_log(log_type, \
        self.now.strftime("%Y-%m-%d %H:%M:%S ") + file_name + message)
