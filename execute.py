from files_updater import programs_updater
from self_update import self_update

#create object for updating modules
selfupdater = self_update()

#if 
if selfupdater.update_modules():
    updater = programs_updater()    
    updater.update()






