from files_updater import programs_updater
from self_update import self_update

#create object for updating modules
selfupdater = self_update()
#create object for updating files
updater = programs_updater()
#check disk availability
isavailable = updater.check_disk()

#if program is updated or update isn't needed - update files
if isavailable:
    mup_success = selfupdater.update_modules()
else:
    mup_success = False
    

if mup_success:
    updater.update()
